from pydantic import BaseModel


class AskRequest(BaseModel):
    file_id: str | None = None
    question: str


class AskResponse(BaseModel):
    file_id: str | None = None
    question: str
    answer: str
