import chromadb
from chromadb import Collection
from backend.config import get_settings

_client = None


def get_chroma_client():
    """Return a singleton persistent ChromaDB client"""
    global _client

    if _client is None:
        settings = get_settings()
        _client = chromadb.PersistentClient(
            path=str(settings.CHROMA_DIR)
        )

    return _client


def _collection_name(file_id: str) -> str:
    """Generate a valid Chroma collection name"""
    # Remove dashes to avoid issues with UUID formatting
    safe_id = file_id.replace("-", "")
    return f"doc_{safe_id}"


def get_or_create_collection(file_id: str) -> Collection:
    """Get or create a Chroma collection for this file_id"""
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=_collection_name(file_id)
    )


def add_chunks(
    file_id: str,
    chunk_ids: list[str],
    embeddings: list[list[float]],
    documents: list[str],
    metadatas: list[dict],
) -> None:
    """Add embedded chunks to the collection"""
    collection = get_or_create_collection(file_id)

    collection.add(
        ids=chunk_ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )


def query_collection(
    file_id: str,
    query_embedding: list[float],
    top_k: int,
) -> dict:
    """Run similarity search, return raw Chroma results"""
    collection = get_or_create_collection(file_id)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    return results


def delete_collection(file_id: str) -> None:
    """Delete a collection by file_id"""
    client = get_chroma_client()
    name = _collection_name(file_id)

    # delete_collection raises if it doesn't exist — guard it
    try:
        client.delete_collection(name=name)
    except Exception:
        pass

