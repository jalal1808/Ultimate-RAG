from fastapi import APIRouter, UploadFile, HTTPException
from backend.storage.file_store import save_upload
from backend.services.pipeline_router import process_upload
from backend.models.upload import UploadResponse

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    try:
        # 1. Save file to disk
        file_id, saved_path = await save_upload(file)
        
        # 2. Extract extension
        extension = file.filename.split(".")[-1].lower() if "." in file.filename else ""
        if not extension:
            raise HTTPException(status_code=400, detail="File has no extension")

        # 3. Process file (extract, chunk, embed, register)
        metadata = process_upload(file_id, saved_path, extension)
        
        return UploadResponse(**metadata)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload processing failed: {e}")
