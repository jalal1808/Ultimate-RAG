import tiktoken
from backend.config import get_settings


def chunk_text(text: str, file_id: str) -> list[dict]:
    """
    Split text into overlapping token-aware chunks.
    Returns list of dicts: {chunk_id, text, token_count, chunk_index}
    """
    settings = get_settings()

    chunk_size = settings.CHUNK_SIZE
    overlap = settings.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("CHUNK_OVERLAP must be smaller than CHUNK_SIZE")

    # 1. Load tokenizer
    enc = tiktoken.get_encoding("cl100k_base")

    # 2. Encode entire text into tokens
    tokens = enc.encode(text)

    if not tokens:
        return []

    # 3. Sliding window setup
    step = chunk_size - overlap

    chunks: list[dict] = []
    chunk_index = 0

    # 4. Slide across token list
    for start in range(0, len(tokens), step):
        end = start + chunk_size
        token_window = tokens[start:end]

        if not token_window:
            break

        # Decode tokens back to string
        chunk_str = enc.decode(token_window)

        chunks.append(
            {
                "chunk_id": f"{file_id}_chunk_{chunk_index}",
                "text": chunk_str,
                "token_count": len(token_window),
                "chunk_index": chunk_index,
            }
        )

        chunk_index += 1

        # Stop if we've reached the end
        if end >= len(tokens):
            break

    return chunks