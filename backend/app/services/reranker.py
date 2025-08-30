import cohere
from typing import List, Dict, Any
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class Reranker:
    def __init__(self):
        self.co = cohere.Client(settings.COHERE_API_KEY)

    def rerank(self, query: str, documents: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
        try:
            texts = [doc['text'] for doc in documents]
            
            response = self.co.rerank(
                model='rerank-english-v3.0',
                query=query,
                documents=texts,
                top_n=top_k
            )
            
            reranked_docs = []
            for result in response.results:
                original_doc = documents[result.index]
                reranked_docs.append({
                    **original_doc,
                    'rerank_score': result.relevance_score
                })
            
            return reranked_docs
        except Exception as e:
            logger.error(f"Error in reranking: {e}")
            # Use original order if reranking fails
            return documents[:top_k]
