from sentence_transformers import CrossEncoder
from backend.config import get_settings

_reranker: CrossEncoder | None = None
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


def _get_reranker() -> CrossEncoder:
    """Lazy-load and cache the cross-encoder model"""
    global _reranker
    if _reranker is None:
        _reranker = CrossEncoder(RERANKER_MODEL)
    return _reranker


def rerank(query: str, chunks: list[dict], top_k: int | None = None) -> list[dict]:
    """
    Rerank chunks by relevance to query.
    chunks: list of dicts with at least a 'text' key
    Returns top_k chunks sorted by rerank score (highest first)
    """
    if not chunks:
        return []

    settings = get_settings()
    top_k = top_k or settings.TOP_K_RERANK

    # Create (query, chunk_text) pairs
    pairs = [(query, chunk["text"]) for chunk in chunks]

    # Get relevance scores
    scores = _get_reranker().predict(pairs)

    # Combine chunks with scores (without mutating input)
    scored = [
        {**chunk, "rerank_score": float(score)}
        for chunk, score in zip(chunks, scores)
    ]

    # Sort by score descending
    scored.sort(key=lambda x: x["rerank_score"], reverse=True)

    return scored[:top_k]