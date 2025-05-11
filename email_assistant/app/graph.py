from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END
from app.agent import summarize_email
from app.memory_store import add_email_to_memory

# 1. Define your State Schema
class EmailState(TypedDict):
    emails: List[Dict] 
    summaries: List[Dict] 

def build_graph():
    graph = StateGraph(EmailState)

    def fetch_emails_node(state):
        from app.email_reader import fetch_unseen_emails
        emails = fetch_unseen_emails()
        state['emails'] = emails
        return state

    def summarize_emails_node(state):
        summaries = []
        for email_obj in state['emails']:
            summary = summarize_email(email_obj['subject'], email_obj['body'])
            summaries.append({"subject": email_obj['subject'], "summary": summary})
        state['summaries'] = summaries
        return state

    def store_in_memory_node(state):
        for email_obj in state['emails']:
            add_email_to_memory(email_obj['subject'], email_obj['body'])
        return state

    graph.add_node("fetch_emails", fetch_emails_node)
    graph.add_node("summarize_emails", summarize_emails_node)
    graph.add_node("store_in_memory", store_in_memory_node)

    graph.set_entry_point("fetch_emails")
    graph.add_edge("fetch_emails", "summarize_emails")
    graph.add_edge("summarize_emails", "store_in_memory")
    graph.add_edge("store_in_memory", END)

    return graph.compile()
