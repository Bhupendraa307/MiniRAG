from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
from typing import List, Dict, Any
from app.config import settings
import uuid
import logging
import time

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        try:
            self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            
            # Create index if needed
            existing_indexes = self.pc.list_indexes().names()
            if settings.PINECONE_INDEX_NAME not in existing_indexes:
                logger.info(f"Creating index: {settings.PINECONE_INDEX_NAME}")
                self.pc.create_index(
                    name=settings.PINECONE_INDEX_NAME,
                    dimension=1536,  # OpenAI ada-002 embedding dimension
                    metric='cosine',
                    spec=ServerlessSpec(
                        cloud='aws',
                        region='us-east-1'
                    )
                )
                # Wait for index
                time.sleep(10)
            
            self.index = self.pc.Index(settings.PINECONE_INDEX_NAME)
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone: {e}")
            raise
        self.openai_client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            timeout=60.0,
            max_retries=3
        )

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.openai_client.embeddings.create(
                    input=texts,
                    model="text-embedding-ada-002"
                )
                return [item.embedding for item in response.data]
            except Exception as e:
                error_str = str(e).lower()
                if "quota" in error_str or "insufficient_quota" in error_str:
                    logger.error(f"OpenAI quota exceeded: {e}")
                    # Return dummy embeddings for fallback
                    return [[0.0] * 1536 for _ in texts]
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"Embedding attempt {attempt + 1} failed, retrying in {wait_time}s: {e}")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Error generating embeddings after {max_retries} attempts: {e}")
                    # Return dummy embeddings as fallback
                    return [[0.0] * 1536 for _ in texts]

    def store_chunks(self, chunks: List[str], metadata: Dict[str, Any]) -> List[str]:
        try:
            embeddings = self.generate_embeddings(chunks)
            chunk_ids = []
            
            vectors = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                chunk_id = str(uuid.uuid4())
                chunk_ids.append(chunk_id)
                
                vectors.append({
                    'id': chunk_id,
                    'values': embedding,
                    'metadata': {
                        **metadata,
                        'text': chunk,
                        'chunk_index': i
                    }
                })
            
            self.index.upsert(vectors)
            return chunk_ids
        except Exception as e:
            logger.error(f"Error storing chunks: {e}")
            raise

    def similarity_search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        try:
            query_embedding = self.generate_embeddings([query])[0]
            
            # Check for dummy embeddings
            if all(x == 0.0 for x in query_embedding):
                logger.warning("Using fallback search")
                # No results available
                return []
            
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            return [
                {
                    'id': match['id'],
                    'score': match['score'],
                    'text': match['metadata']['text'],
                    'metadata': match['metadata']
                }
                for match in results['matches']
            ]
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            return []