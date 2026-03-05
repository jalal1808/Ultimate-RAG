import pandas as pd

_registry: dict[str, pd.DataFrame] = {}


def register(file_id: str, df: pd.DataFrame) -> None:
    """Store a DataFrame for this file_id"""
    _registry[file_id] = df


def get(file_id: str) -> pd.DataFrame | None:
    """Retrieve the DataFrame for this file_id"""
    return _registry.get(file_id)


def is_registered(file_id: str) -> bool:
    """Check if a DataFrame exists for this file_id"""
    return file_id in _registry


def unregister(file_id: str) -> None:
    """Remove a DataFrame from the registry"""
    _registry.pop(file_id, None)
