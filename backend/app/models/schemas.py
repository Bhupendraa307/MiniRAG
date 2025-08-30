from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UploadRequest(BaseModel):
    text: Optional[str] = None
    filename: Optional[str] = None

class QueryRequest(BaseModel):
    query: str

class Citation(BaseModel):
    id: str
    text: str
    metadata: dict

class QueryResponse(BaseModel):
    answer: str
    citations: List[Citation]
    token_usage: dict
    latency: float

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime

class UploadResponse(BaseModel):
    message: str
    document_id: str
    filename: str