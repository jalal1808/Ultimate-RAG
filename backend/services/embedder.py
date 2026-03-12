from sentence_transformers import SentenceTransformer
from backend.config import get_settings

_model: SentenceTransformer | None = None


def _get_model() -> SentenceTransformer:
    """Lazy-load and cache the local embedding model"""
    global _model
    if _model is None:
        settings = get_settings()
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
    return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Embed a list of text strings.
    Returns list of embedding vectors (one per text).
    """
    if not texts:
        return []

    settings = get_settings()

    if settings.EMBEDDING_PROVIDER == "local":
        model = _get_model()
        vectors = model.encode(
            texts,
            batch_size=32,
            show_progress_bar=False,
        )
        return [v.tolist() for v in vectors]

    if settings.EMBEDDING_PROVIDER == "openai":
        # Stub for future implementation
        raise NotImplementedError("OpenAI embedding provider not implemented yet")

    raise NotImplementedError(
        f"Provider {settings.EMBEDDING_PROVIDER!r} not implemented"
    )


def embed_query(query: str) -> list[float]:
    """
    Embed a single query string.
    Returns a single embedding vector.
    """
    if not query:
        raise ValueError("Query must not be empty")

    return embed_texts([query])[0]