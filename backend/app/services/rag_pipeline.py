# from typing import List, Dict, Any, Tuple
# from app.services.vector_store import VectorStore
# from app.services.reranker import Reranker
# from app.services.llm import LLMService
# from app.services.database import DatabaseService
# from app.utils.text_processing import chunk_text
# from app.config import settings
# import logging

# logger = logging.getLogger(__name__)

# class RAGPipeline:
#     def __init__(self):
#         self.vector_store = VectorStore()
#         self.reranker = Reranker()
#         self.llm = LLMService()
#         self.db = DatabaseService()

#     def process_document(self, text: str, filename: str) -> str:
#         try:
#             # Chunk the text
#             chunks = chunk_text(text, settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)
            
#             try:
#                 # Try to store chunks in vector database
#                 metadata = {
#                     'filename': filename,
#                     'total_chunks': len(chunks)
#                 }
#                 chunk_ids = self.vector_store.store_chunks(chunks, metadata)
#                 doc_id = self.db.store_document_metadata(filename, chunk_ids, metadata)
#                 logger.info(f"Processed document {filename} with {len(chunks)} chunks using embeddings")
#             except Exception as embed_error:
#                 logger.warning(f"Embedding storage failed, using text fallback: {embed_error}")
#                 # Fallback to text-only storage
#                 doc_id = self.db.store_text_chunks(filename, chunks)
#                 logger.info(f"Processed document {filename} with {len(chunks)} chunks using text fallback")
            
#             return doc_id
            
#         except Exception as e:
#             logger.error(f"Error processing document: {e}")
#             raise

#     def query(self, query: str) -> Tuple[str, List[Dict[str, Any]], dict, float]:
#         try:
#             # Try vector search first
#             retrieved_docs = self.vector_store.similarity_search(query, settings.TOP_K)
            
#             # If no results from vector search, try text fallback
#             if not retrieved_docs:
#                 logger.info("No vector results, trying text search fallback")
#                 retrieved_docs = self.db.search_text_chunks(query, settings.TOP_K)
            
#             if not retrieved_docs:
#                 return "I couldn't find relevant information to answer your question.", [], {}, 0.0
            
#             # Rerank documents (skip if using text fallback)
#             if retrieved_docs and 'rerank_score' not in retrieved_docs[0]:
#                 try:
#                     reranked_docs = self.reranker.rerank(query, retrieved_docs, settings.RERANK_TOP_K)
#                 except Exception as rerank_error:
#                     logger.warning(f"Reranking failed, using original order: {rerank_error}")
#                     reranked_docs = retrieved_docs[:settings.RERANK_TOP_K]
#             else:
#                 reranked_docs = retrieved_docs[:settings.RERANK_TOP_K]
            
#             # Generate answer with LLM
#             answer, token_usage, latency = self.llm.generate_answer(query, reranked_docs)
            
#             # Prepare citations
#             citations = [
#                 {
#                     'id': doc['id'],
#                     'text': doc['text'][:200] + "..." if len(doc['text']) > 200 else doc['text'],
#                     'full_text': doc['text'],
#                     'metadata': doc['metadata']
#                 }
#                 for doc in reranked_docs
#             ]
            
#             # Log query
#             self.db.log_query(query, answer, citations, token_usage, latency)
            
#             return answer, citations, token_usage, latency
            
#         except Exception as e:
#             logger.error(f"Error in query processing: {e}")
#             raise




# ?++   Gemin

from typing import List, Dict, Any, Tuple
from app.services.vector_store import VectorStore
from app.services.reranker import Reranker
from app.services.llm import LLMService
from app.services.database import DatabaseService
from app.utils.text_processing import chunk_text
from app.utils.security import clean_for_log
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self):
        self.vector_store = VectorStore()
        self.reranker = Reranker()
        self.llm = LLMService()
        self.db = DatabaseService()

    def process_document(self, text: str, filename: str) -> str:
        try:
            # Chunk the text
            chunks = chunk_text(text, settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)
            
            try:
                # Try to store chunks in vector database
                metadata = {
                    'filename': filename,
                    'total_chunks': len(chunks)
                }
                chunk_ids = self.vector_store.store_chunks(chunks, metadata)
                doc_id = self.db.store_document_metadata(filename, chunk_ids, metadata)
                logger.info(f"Processed {clean_for_log(filename)} - {len(chunks)} chunks")
            except Exception as embed_error:
                logger.warning(f"Embedding storage failed, using text fallback: {embed_error}")
                # Fallback to text-only storage
                doc_id = self.db.store_text_chunks(filename, chunks)
                logger.info(f"Processed {clean_for_log(filename)} - {len(chunks)} chunks (text mode)")
            
            return doc_id
            
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            raise

    def query(self, query: str) -> Tuple[str, List[Dict[str, Any]], dict, float]:
        try:
            # Try vector search first
            retrieved_docs = self.vector_store.similarity_search(query, settings.TOP_K)
            
            # If no results from vector search, try text fallback
            if not retrieved_docs:
                logger.info("No vector results, trying text search fallback")
                retrieved_docs = self.db.search_text_chunks(query, settings.TOP_K)
            
            if not retrieved_docs:
                return "I couldn't find relevant information to answer your question.", [], {}, 0.0
            
            # Rerank documents if applicable
            if retrieved_docs and 'rerank_score' not in retrieved_docs[0]:
                try:
                    reranked_docs = self.reranker.rerank(query, retrieved_docs, settings.RERANK_TOP_K)
                except Exception as rerank_error:
                    logger.warning(f"Reranking failed, using original order: {rerank_error}")
                    reranked_docs = retrieved_docs[:settings.RERANK_TOP_K]
            else:
                reranked_docs = retrieved_docs[:settings.RERANK_TOP_K]
            
            # Generate answer with LLM
            answer, token_usage, latency = self.llm.generate_answer(query, reranked_docs)
            
            # Prepare citations
            citations = [
                {
                    'id': doc['id'],
                    # CORRECTED: Send the full, untrimmed text.
                    # The frontend will handle creating previews.
                    'text': doc['text'],
                    'metadata': doc['metadata']
                }
                for doc in reranked_docs
            ]
            
            # Log query
            self.db.log_query(query, answer, citations, token_usage, latency)
            
            return answer, citations, token_usage, latency
            
        except Exception as e:
            logger.error(f"Error in query processing: {e}")
            raise