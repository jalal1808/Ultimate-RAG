from pydantic import BaseModel

class SummarizeRequest(BaseModel):
    file_id: str

class SummarizeResponse(BaseModel):
    file_id: str
    summary: str
