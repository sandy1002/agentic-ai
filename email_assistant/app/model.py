from pydantic import BaseModel

class EmailSummaryRequest(BaseModel):
    subject: str
    body: str

class SummarizedEmail(BaseModel):
    summary: str

class ReplySuggestion(BaseModel):
    email_content: str