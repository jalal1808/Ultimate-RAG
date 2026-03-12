from pathlib import Path


def get_file_extension(filename: str) -> str:
    """Return lowercased extension e.g. 'pdf', 'csv'"""
    if not filename:
        raise ValueError("Filename is required")

    ext = Path(filename).suffix.lower().lstrip(".")
    if not ext:
        raise ValueError("File has no extension")

    return ext


def detect_file_type(filename: str, content_type: str | None) -> str:
    """Returns 'text' or 'table' based on file extension"""
    ext = get_file_extension(filename)

    text_extensions = {"pdf", "docx", "txt", "md"}
    table_extensions = {"csv", "xlsx"}

    if ext in text_extensions:
        return "text"
    if ext in table_extensions:
        return "table"

    raise ValueError(f"Unsupported file type: .{ext}")