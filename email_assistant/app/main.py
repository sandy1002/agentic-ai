from fastapi import FastAPI
from app.model import EmailSummaryRequest, SummarizedEmail
from app.agent import summarize_email
from app.graph import build_graph

app = FastAPI(title="Email Assistant POC", version="0.1")

@app.get("/")
def root():
    return {"message": "Email Assistant is running 🚀"}

@app.post("/summarize", response_model=SummarizedEmail)
def summarize(request: EmailSummaryRequest):
    result = summarize_email(request.subject, request.body)
    return SummarizedEmail(summary=result)

@app.get("/process-inbox")
def process_inbox():
    graph = build_graph()
    final_state = graph.invoke({})
    return {"message": "Inbox processed", "state": final_state}
