from pydantic import BaseModel

class EmailSummaryRequest(BaseModel):
    subject: str
    body: str

class SummarizedEmail(BaseModel):
    summary: str
