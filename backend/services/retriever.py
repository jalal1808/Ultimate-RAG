from backend.storage import chroma_store
from backend.config import get_settings


def retrieve_chunks(
    query_embedding: list[float],
    file_id: str | None = None,
    top_k: int | None = None,
) -> list[dict]:
    """
    Query Chroma for top_k similar chunks.
    If file_id is provided, scopes search to that file.
    If file_id is None, searches across all documents.
    Returns list of dicts: {chunk_id, text, metadata, distance}
    """
    settings = get_settings()
    top_k = top_k or settings.TOP_K_RETRIEVAL

    # Build optional metadata filter
    where = {"file_id": file_id} if file_id else None

    results = chroma_store.query_collection(
        query_embedding=query_embedding,
        top_k=top_k,
        where=where,
    )

    if not results:
        return []

    ids_list = results.get("ids")
    docs_list = results.get("documents")
    metas_list = results.get("metadatas")
    distances_list = results.get("distances")

    # Guard against empty or malformed results
    if not ids_list or not ids_list[0]:
        return []

    ids = ids_list[0]
    docs = docs_list[0] if docs_list else []
    metas = metas_list[0] if metas_list else []
    distances = distances_list[0] if distances_list else []

    return [
        {
            "chunk_id": chunk_id,
            "text": doc,
            "metadata": meta,
            "distance": dist,
        }
        for chunk_id, doc, meta, dist in zip(ids, docs, metas, distances)
    ]
