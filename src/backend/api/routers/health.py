from fastapi import APIRouter
from pydantic import BaseModel
from src.settings import custom_logger

logger = custom_logger("API Health")

health_router = APIRouter()


class HealthResponse(BaseModel):
    status: str = "ok"


@health_router.get(
    "/health",
    summary="Health check",
    response_description="Estado del servicio.",
)
def get_health() -> HealthResponse:
    """Retorna `{"status": "ok"}` cuando el servicio está funcionando correctamente."""
    return HealthResponse()
