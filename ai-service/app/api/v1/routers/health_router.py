from fastapi import APIRouter
from app.api.v1.schemas import HealthStatusDto

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=HealthStatusDto)
def health_check():
    return HealthStatusDto(status="healthy")
