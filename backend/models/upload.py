from pydantic import BaseModel


class UploadResponse(BaseModel):
    file_id: str
    filename: str
    file_type: str
    chunks: int
    rows: int
    cols: int
    duplicate_of: str | None = None
