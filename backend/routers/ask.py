from fastapi import APIRouter, HTTPException
from backend.services.pipeline_router import get_answer
from backend.models.ask import AskRequest, AskResponse

router = APIRouter()

@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    try:
        answer_text = get_answer(request.file_id, request.question)
        return AskResponse(
            file_id=request.file_id,
            question=request.question,
            answer=answer_text
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Question answering failed: {e}")
