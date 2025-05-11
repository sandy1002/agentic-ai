from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.config import OPENAI_API_KEY
from langchain_community.llms import Ollama

# llm = OpenAI(api_key=OPENAI_API_KEY, temperature=0.3)
llm = Ollama(model="llama3")

def summarize_email(subject, body):
    prompt_template = PromptTemplate(
        input_variables=["subject", "body"],
        template="Summarize the following email with subject: {subject}\n\n{body}\n\nSummary:"
    )
    chain = LLMChain(llm=llm, prompt=prompt_template)
    result = chain.run({"subject": subject, "body": body})
    return result
