from fastapi import APIRouter
from app.models.schemas import HealthResponse
from app.utils.security import utc_now

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        timestamp=utc_now()
    )