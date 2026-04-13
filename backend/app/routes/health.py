from fastapi import APIRouter # type: ignore
from datetime import datetime

router = APIRouter()

@router.get("/")
def health_check():
    """
    Health check endpoint.
    Used for monitoring system availability.
    """
    return {
        "status": "ok",
        "timestamp": datetime.utcnow(),
        "service": "QR Payment Security API"
    }