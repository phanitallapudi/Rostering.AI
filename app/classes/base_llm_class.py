from langchain_openai import AzureOpenAIEmbeddings
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv

import os

class BaseLLMRequirements:
    def __init__(self) -> None:
        load_dotenv()

    def openai_key_environ(self):
        os.environ["AZURE_OPENAI_API_KEY"] = os.getenv('AZURE_OPENAI_API_KEY')
        os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv('AZURE_OPENAI_ENDPOINT')
    
    def get_llm(self):
        return AzureChatOpenAI(
            openai_api_version="2023-12-01-preview",
            azure_deployment="ailm",
            max_tokens=16000,
            temperature = 0.5
        )
    
    def get_embeddings(self):
        return AzureOpenAIEmbeddings(
            azure_endpoint=os.getenv('AZURE_OPENAI_EMBEDDINGS_ENDPOINT'),
            openai_api_key=os.getenv('AZURE_OPENAI_EMBEDDINGS_API_KEY'),
            azure_deployment="embedding-model",
            openai_api_version="2023-03-15-preview",
            model="text-embedding-ada-002"
        )

    