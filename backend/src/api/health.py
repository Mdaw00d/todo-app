"""Health check endpoint."""

from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    timestamp: datetime


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Return the health status of the API."""
    return HealthResponse(status="healthy", timestamp=datetime.utcnow())
