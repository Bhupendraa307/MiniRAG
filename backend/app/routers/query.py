from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse, Citation
from app.services.rag_pipeline import RAGPipeline
from app.utils.security import clean_for_log
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
rag_pipeline = RAGPipeline()

@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    try:
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        query = request.query.strip()
        if len(query) > 1000:
            raise HTTPException(status_code=400, detail="Query too long")
        
        answer, citations_data, token_usage, latency = rag_pipeline.query(query)
        
        citations = [
            Citation(
                id=cite['id'],
                text=cite['text'],
                metadata=cite['metadata']
            )
            for cite in citations_data
        ]
        
        return QueryResponse(
            answer=answer,
            citations=citations,
            token_usage=token_usage,
            latency=latency
        )
        
    except Exception as e:
        logger.error(f"Query error: {clean_for_log(str(e))}")
        raise HTTPException(status_code=500, detail=str(e))