import uuid
import aiofiles
from pathlib import Path
from fastapi import UploadFile
from backend.config import get_settings


async def save_upload(file: UploadFile) -> tuple[str, Path]:
    """Save uploaded file, return (file_id, saved_path)"""
    settings = get_settings()

    # Ensure upload directory exists
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Generate unique file ID
    file_id = str(uuid.uuid4())

    # Preserve original filename (fallback if missing)
    original_name = file.filename or "uploaded_file"

    # Encode file_id into filename
    saved_filename = f"{file_id}_{original_name}"
    saved_path = upload_dir / saved_filename

    # Async write file to disk
    async with aiofiles.open(saved_path, "wb") as out_file:
        while chunk := await file.read(1024 * 1024): 
            await out_file.write(chunk)

    # Reset file pointer (optional but often useful)
    await file.seek(0)

    return file_id, saved_path


def get_file_path(file_id: str, filename: str) -> Path:
    """Reconstruct path from file_id + original filename"""
    settings = get_settings()

    upload_dir = Path(settings.UPLOAD_DIR)
    saved_filename = f"{file_id}_{filename}"

    return upload_dir / saved_filename

