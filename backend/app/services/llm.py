from openai import OpenAI
from typing import List, Dict, Any, Tuple
from app.config import settings
import logging
import time

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_answer(self, query: str, context_docs: List[Dict[str, Any]]) -> Tuple[str, dict, float]:
        try:
            context = self._format_context(context_docs)
            
            prompt = f"""Based on the following context, answer the user's question. Include inline citations using [1], [2], etc. format for each source used.

Context:
{context}

Question: {query}

Answer with citations:"""

            start_time = time.time()
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context. Always include inline citations [1], [2], etc. when referencing sources."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            latency = time.time() - start_time
            
            answer = response.choices[0].message.content
            token_usage = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens
            }
            
            return answer, token_usage, latency
            
        except Exception as e:
            error_str = str(e).lower()
            if "quota" in error_str or "insufficient_quota" in error_str:
                logger.error(f"OpenAI quota exceeded for LLM: {e}")
                # Return a simple concatenated answer from context
                fallback_answer = self._generate_fallback_answer(query, context_docs)
                return fallback_answer, {'total_tokens': 0}, 0.1
            logger.error(f"Error generating answer: {e}")
            raise
    
    def _generate_fallback_answer(self, query: str, context_docs: List[Dict[str, Any]]) -> str:
        if not context_docs:
            return "Found some information but can't generate answer right now."
        
        answer_parts = []
        for i, doc in enumerate(context_docs[:3], 1):
            text = doc['text'][:300] + "..." if len(doc['text']) > 300 else doc['text']
            answer_parts.append(f"[{i}] {text}")
        
        return "Based on available info:\n\n" + "\n\n".join(answer_parts)

    def _format_context(self, docs: List[Dict[str, Any]]) -> str:
        context_parts = []
        for i, doc in enumerate(docs, 1):
            context_parts.append(f"[{i}] {doc['text']}")
        return "\n\n".join(context_parts)