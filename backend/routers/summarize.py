from fastapi import APIRouter, HTTPException
from backend.services.pipeline_router import get_summary
from backend.models.summarize import SummarizeRequest, SummarizeResponse

router = APIRouter()

@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_document(request: SummarizeRequest):
    try:
        summary_text = get_summary(request.file_id)
        return SummarizeResponse(
            file_id=request.file_id,
            summary=summary_text
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {e}")
