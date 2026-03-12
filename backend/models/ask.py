from pydantic import BaseModel

class AskRequest(BaseModel):
    file_id: str
    question: str

class AskResponse(BaseModel):
    file_id: str
    question: str
    answer: str
