from fastapi import FastAPI

from src.api.routers.health import health_router
from src.api.routers.poperty_value import properties_classification_router


def init_routers(app: FastAPI) -> None:
    """
    Function for initializing the routers of the API.

    Args:
        app: FastAPI application instance
    """

    app.include_router(health_router)
    app.include_router(properties_classification_router, prefix="/properties-valuation")
