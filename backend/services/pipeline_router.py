import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

from backend.storage import chroma_store, file_store
from backend.services import (
    text_extractor,
    text_chunker,
    embedder,
    retriever,
    reranker,
    generator,
    summarizer,
    table_reasoner,
)
from backend.registries import vector_registry, dataframe_registry, summary_registry

# Metadata store: file_id -> {filename, extension, file_type}
_file_metadata: dict[str, dict] = {}


def process_upload(file_id: str, file_path: Path, extension: str) -> dict:
    """
    Run the correct ingestion pipeline based on file type.
    Includes content-hash deduplication for text files.
    Returns processing metadata.
    """
    extension = extension.lower().lstrip(".")

    if extension in {"pdf", "docx", "txt", "md"}:
        file_type = "text"
    elif extension in {"csv", "xlsx"}:
        file_type = "table"
    else:
        raise ValueError(f"Unsupported file extension: .{extension}")

    # Extract original filename (strip the file_id prefix)
    original_name = file_path.name
    prefix = f"{file_id}_"
    if original_name.startswith(prefix):
        original_name = original_name[len(prefix):]

    # Store metadata for later use (summarize, answer)
    _file_metadata[file_id] = {
        "filename": original_name,
        "extension": extension,
        "file_type": file_type,
    }

    if file_type == "text":
        # --- Deduplication check ---
        content_hash = file_store.compute_file_hash(file_path)

        existing_file_id = chroma_store.get_file_id_by_hash(content_hash)
        if existing_file_id:
            # File already ingested — register this file_id but skip re-processing
            vector_registry.register(file_id, content_hash)
            return {
                "file_id": file_id,
                "file_type": file_type,
                "filename": original_name,
                "chunks": 0,
                "rows": 0,
                "cols": 0,
                "duplicate_of": existing_file_id,
            }

        # 1. Extract text
        text = text_extractor.extract_text(file_path, extension)

        # 2. Chunk
        chunks = text_chunker.chunk_text(text, file_id=file_id)

        # 3. Embed (batch)
        texts = [chunk["text"] for chunk in chunks]
        embeddings = embedder.embed_texts(texts)

        # 4. Build enriched metadata for each chunk
        upload_date = datetime.now(timezone.utc).isoformat()
        chunk_ids = [chunk["chunk_id"] for chunk in chunks]
        metadatas = [
            {
                "file_id": file_id,
                "filename": original_name,
                "file_type": file_type,
                "chunk_index": chunk["chunk_index"],
                "content_hash": content_hash,
                "upload_date": upload_date,
            }
            for chunk in chunks
        ]

        # 5. Store in Chroma (single collection)
        chroma_store.add_chunks(chunk_ids, embeddings, texts, metadatas)

        # 6. Register in vector registry
        vector_registry.register(file_id, content_hash)

        return {
            "file_id": file_id,
            "file_type": file_type,
            "filename": original_name,
            "chunks": len(chunks),
            "rows": 0,
            "cols": 0,
        }

    else:  # table
        # Load DataFrame
        if extension == "csv":
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        # Register in dataframe registry
        dataframe_registry.register(file_id, df)

        return {
            "file_id": file_id,
            "file_type": file_type,
            "filename": original_name,
            "chunks": 0,
            "rows": len(df),
            "cols": len(df.columns),
        }


def get_summary(file_id: str) -> str:
    """
    Check summary cache first, then generate and cache.
    """
    # Cache hit
    if summary_registry.is_cached(file_id):
        return summary_registry.get(file_id)

    meta = _file_metadata.get(file_id)
    if not meta:
        raise ValueError(f"No metadata found for file_id={file_id!r}. Was it uploaded?")

    file_type = meta["file_type"]

    if file_type == "text":
        path = file_store.get_file_path(file_id, meta["filename"])
        text = text_extractor.extract_text(path, meta["extension"])
        result = summarizer.summarize_text(text)

    elif file_type == "table":
        df = dataframe_registry.get(file_id)
        if df is None:
            raise ValueError(f"No DataFrame registered for file_id={file_id!r}")
        result = summarizer.summarize_table(df)

    else:
        raise ValueError(f"Unsupported file_type: {file_type!r}")

    summary_registry.cache(file_id, result)
    return result


def get_answer(file_id: str | None, question: str) -> str:
    """
    Route to text RAG or table reasoning based on registries.
    If file_id is None, search across all documents.
    """
    if file_id is None:
        # --- Cross-document RAG pipeline ---
        query_embedding = embedder.embed_query(question)
        chunks = retriever.retrieve_chunks(query_embedding, file_id=None)

        if not chunks:
            return "No relevant content found across any documents."

        chunks = reranker.rerank(question, chunks)
        return generator.generate_answer(question, chunks)

    if vector_registry.is_registered(file_id):
        # --- Text RAG pipeline (scoped to one file) ---
        query_embedding = embedder.embed_query(question)
        chunks = retriever.retrieve_chunks(query_embedding, file_id=file_id)

        if not chunks:
            return "No relevant content found in the document."

        chunks = reranker.rerank(question, chunks)
        return generator.generate_answer(question, chunks)

    elif dataframe_registry.is_registered(file_id):
        # --- Table reasoning pipeline ---
        df = dataframe_registry.get(file_id)
        return table_reasoner.answer_from_table(question, df)

    else:
        raise ValueError(
            f"file_id={file_id!r} is not registered. "
            "Please upload the file first via POST /upload"
        )
