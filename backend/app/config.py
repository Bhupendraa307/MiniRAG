import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "mini-rag-index")
    MONGODB_URI = os.getenv("MONGODB_URI")
    MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "mini_rag_db")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 150
    TOP_K = 10
    RERANK_TOP_K = 5

settings = Settings()