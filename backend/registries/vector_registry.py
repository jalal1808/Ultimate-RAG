_registry: dict[str, dict] = {}


def register(file_id: str, content_hash: str = "") -> None:
    """Mark a file_id as having chunks in Chroma, with its content hash"""
    _registry[file_id] = {"content_hash": content_hash}


def is_registered(file_id: str) -> bool:
    """Check if a vector collection exists for this file_id"""
    return file_id in _registry


def get_file_id_by_hash(content_hash: str) -> str | None:
    """Find existing file_id for a given content hash"""
    for fid, meta in _registry.items():
        if meta.get("content_hash") == content_hash:
            return fid
    return None


def unregister(file_id: str) -> None:
    """Remove a file_id from the vector registry"""
    _registry.pop(file_id, None)
