_registry: dict[str, str] = {}


def register(file_id: str) -> None:
    """Mark a file_id as having a vector collection in Chroma"""
    _registry[file_id] = file_id


def is_registered(file_id: str) -> bool:
    """Check if a vector collection exists for this file_id"""
    return file_id in _registry


def unregister(file_id: str) -> None:
    """Remove a file_id from the vector registry"""
    _registry.pop(file_id, None)
