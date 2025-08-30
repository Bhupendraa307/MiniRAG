from pymongo import MongoClient
from typing import Dict, Any, List
from app.config import settings
from app.utils.security import clean_for_log, utc_now
import logging

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.client = MongoClient(settings.MONGODB_URI)
        self.db = self.client[settings.MONGODB_DB_NAME]
        self.documents = self.db.documents
        self.queries = self.db.queries
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def store_document_metadata(self, filename: str, chunk_ids: List[str], metadata: Dict[str, Any]) -> str:
        try:
            doc = {
                'filename': filename,
                'chunk_ids': chunk_ids,
                'metadata': metadata,
                'created_at': utc_now()
            }
            result = self.documents.insert_one(doc)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error storing document metadata: {e}")
            raise
    
    def store_text_chunks(self, filename: str, chunks: List[str]) -> str:
        try:
            doc = {
                'filename': filename,
                'chunks': chunks,
                'storage_type': 'text_fallback',
                'created_at': utc_now()
            }
            result = self.documents.insert_one(doc)
            logger.info(f"Stored {len(chunks)} text chunks for {clean_for_log(filename)}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error storing text chunks: {e}")
            raise
    
    def search_text_chunks(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        try:
            query_words = query.lower().split()
            results = []
            
            docs = list(self.documents.find({'storage_type': 'text_fallback'}))
            
            for doc in docs:
                chunks = doc.get('chunks', [])
                for i, chunk in enumerate(chunks):
                    chunk_lower = chunk.lower()
                    score = sum(1 for word in query_words if word in chunk_lower)
                    if score > 0:
                        results.append({
                            'id': f"{doc['_id']}_{i}",
                            'text': chunk,
                            'score': score / len(query_words),
                            'metadata': {'filename': doc['filename'], 'chunk_index': i}
                        })
            
            logger.info(f"Found {len(results)} results for: {clean_for_log(query)}")
            results.sort(key=lambda x: x['score'], reverse=True)
            return results[:limit]
        except Exception as e:
            logger.error(f"Text search error: {e}")
            return []

    def log_query(self, query: str, answer: str, citations: List[Dict], token_usage: dict, latency: float):
        try:
            query_log = {
                'query': query,
                'answer': answer,
                'citations': citations,
                'token_usage': token_usage,
                'latency': latency,
                'timestamp': utc_now()
            }
            self.queries.insert_one(query_log)
        except Exception as e:
            logger.error(f"Error logging query: {e}")

    def get_document_by_id(self, doc_id: str) -> Dict[str, Any]:
        try:
            return self.documents.find_one({'_id': doc_id})
        except Exception as e:
            logger.error(f"Error retrieving document: {e}")
            return None
    
    def close(self):
        if hasattr(self, 'client'):
            self.client.close()