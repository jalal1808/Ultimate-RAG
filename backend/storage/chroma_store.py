import chromadb
from chromadb import Collection
from backend.config import get_settings

_client = None

COLLECTION_NAME = "rag_documents"


def get_chroma_client():
    """Return a singleton persistent ChromaDB client"""
    global _client

    if _client is None:
        settings = get_settings()
        _client = chromadb.PersistentClient(
            path=str(settings.CHROMA_DIR)
        )

    return _client


def get_collection() -> Collection:
    """Get or create the single unified collection"""
    client = get_chroma_client()
    return client.get_or_create_collection(name=COLLECTION_NAME)


def add_chunks(
    chunk_ids: list[str],
    embeddings: list[list[float]],
    documents: list[str],
    metadatas: list[dict],
) -> None:
    """Add embedded chunks to the unified collection"""
    collection = get_collection()

    collection.add(
        ids=chunk_ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )


def query_collection(
    query_embedding: list[float],
    top_k: int,
    where: dict | None = None,
) -> dict:
    """Run similarity search with optional metadata filters"""
    collection = get_collection()

    kwargs = {
        "query_embeddings": [query_embedding],
        "n_results": top_k,
    }

    if where:
        kwargs["where"] = where

    return collection.query(**kwargs)


def delete_by_file_id(file_id: str) -> None:
    """Delete all chunks belonging to a specific file_id"""
    collection = get_collection()

    try:
        collection.delete(where={"file_id": file_id})
    except Exception:
        pass


def has_content_hash(content_hash: str) -> bool:
    """Check if chunks with this content hash already exist"""
    collection = get_collection()

    results = collection.get(
        where={"content_hash": content_hash},
        limit=1,
    )

    return bool(results and results.get("ids"))


def get_file_id_by_hash(content_hash: str) -> str | None:
    """Find existing file_id for a given content hash"""
    collection = get_collection()

    results = collection.get(
        where={"content_hash": content_hash},
        limit=1,
    )

    if results and results.get("metadatas") and results["metadatas"]:
        return results["metadatas"][0].get("file_id")

    return None
