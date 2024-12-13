from langchain_huggingface import HuggingFaceEndpoint

from dotenv import load_dotenv

load_dotenv()

# Setting up the Hugging Face model endpoint
repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
llm = HuggingFaceEndpoint(repo_id=repo_id, max_length=128, temperature=0.7, token="HUGGINGFACE_API_KEY")

PROMPT_GUIDELINES = """
Please keep your responses compact and relevant. Respond only based on the following topics:
- Trip planning based on RV specifications.
- Suggested routes for specific terrains (e.g., hills, beaches).
- Finding nearby campgrounds, RV parks, or fuel stations.
- Locating RV technicians and repair services.
- Informing users about route constraints (e.g., low bridges, diesel availability).
"""
from langchain import PromptTemplate, LLMChain

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])
print(prompt)

def ask_emily_query(user_input):
    prompt = f"{PROMPT_GUIDELINES}\nUser input: {user_input}"
    response = llm.invoke(prompt)
    return response
