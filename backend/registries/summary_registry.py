_registry: dict[str, str] = {}


def cache(file_id: str, summary: str) -> None:
    """Cache a generated summary for this file_id"""
    _registry[file_id] = summary


def get(file_id: str) -> str | None:
    """Retrieve a cached summary, or None if not cached"""
    return _registry.get(file_id)


def is_cached(file_id: str) -> bool:
    """Check if a summary is cached for this file_id"""
    return file_id in _registry


def invalidate(file_id: str) -> None:
    """Remove a cached summary (e.g. after re-upload)"""
    _registry.pop(file_id, None)

