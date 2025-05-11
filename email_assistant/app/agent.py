from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
# from app.config import OPENAI_API_KEY
from langchain_community.llms import Ollama

# llm = OpenAI(api_key=OPENAI_API_KEY, temperature=0.3)
llm = Ollama(model="llama3")
reply_prompt = PromptTemplate.from_template(
    "You are an email assistant. Read the email below and generate a professional and concise reply.\n\nEmail:\n{email_content}\n\nReply:"
)

def summarize_email(subject, body):
    prompt_template = PromptTemplate(
        input_variables=["subject", "body"],
        template="Summarize the following email with subject: {subject}\n\n{body}\n\nSummary:"
    )
    chain = LLMChain(llm=llm, prompt=prompt_template)
    result = chain.run({"subject": subject, "body": body})
    return result

def suggest_reply(email_content: str) -> str:
    prompt = reply_prompt.format(email_content=email_content)
    return llm.invoke(prompt)
