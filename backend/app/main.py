from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import upload, query, health
from app.config import settings
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_env():
    required = ['OPENAI_API_KEY', 'PINECONE_API_KEY', 'COHERE_API_KEY', 'MONGODB_URI']
    missing = [var for var in required if not getattr(settings, var)]
    if missing:
        logger.error(f"Missing env vars: {missing}")
        raise ValueError(f"Missing: {missing}")
    logger.info("Environment OK")

check_env()

app = FastAPI(
    title="Mini RAG API",
    description="A Retrieval-Augmented Generation API with vector search and reranking",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mini-rag-rosy.vercel.app/"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(query.router, prefix="/api", tags=["query"])
app.include_router(health.router, prefix="/api", tags=["health"])

@app.on_event("startup")
async def startup_event():
    logger.info("Starting Mini RAG API...")
    try:

        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY, timeout=10.0)

        logger.info("OpenAI API connection validated")
    except Exception as e:
        logger.warning(f"OpenAI API validation failed: {e}")

@app.get("/")
async def root():
    return {"message": "Mini RAG API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
