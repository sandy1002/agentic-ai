# import chromadb
# from chromadb.config import Settings

# chroma_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chroma_db"))

# collection = chroma_client.get_or_create_collection(name="email_memory")

# def add_email_to_memory(subject, body):
#     collection.add(
#         documents=[body],
#         metadatas=[{"subject": subject}],
#         ids=[subject]  # simple way using subject as ID
#     )

# def search_similar_emails(query_text):
#     return collection.query(query_texts=[query_text], n_results=3)


# TEMPORARY for POC
email_memory = {}

def add_email_to_memory(subject, body):
    email_memory[subject] = body

def search_similar_emails(query_text):
    return {k: v for k, v in email_memory.items() if query_text.lower() in v.lower()}
