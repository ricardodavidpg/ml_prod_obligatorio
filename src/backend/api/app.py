from contextlib import asynccontextmanager
import os
import sys
from typing import Dict, Any, AsyncGenerator

sys.path.append(os.getcwd())

import uvicorn

from src.api.routers import init_routers
from src.settings import custom_logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


logger = custom_logger("API")


# Context manager, inicializa el preprocesador y el clasificador cuando se levanta la app
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Function for loading the classifier, preprocessor and settings on startup

    Args:
        app: FastAPI application instance

    Returns:
        Dictionary containing the classifier, preprocessor and settings
    """
    try:
        logger.info("Starting up application...")

        # TODO: Definir el startup de la applicación una vez tengamos hecho el clasificador

        """settings = SettingsManager()
        preprocessor = Preprocessor()
        classifier = Classifier(
            model_id=settings.MODEL_ID,
            batch_size=settings.BATCH_SIZE,
        )"""
        """logger.info("Application startup complete")"""
        """yield {
            "settings": settings,
            "preprocessor": preprocessor,
            "classifier": classifier,
        }"""
        yield
            # TODO: Definir el yield con lo que querramos mantener en scope global
        
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise
    finally:
        logger.info("Shutting down application...")

app = FastAPI(
    title="Obligatorio Machine Learning en Producción - 2026",
    description="API para el Obligatorio de Machine Learning en Producción 2026",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Para evitar problemas de seguridad se habilita cualquier origen de solicitud
    allow_methods=["*"],  # se debería restringir esto a los dominios necesarios
    allow_headers=["*"],
)

# Cargar routers, estos son /health /properies/houses
init_routers(app)


#Punto de entrada para correr la app con uvicorn, se puede correr con `uvicorn src.api.app:app --reload`
if __name__ == "__main__":
    uvicorn.run(
        "src.api.app:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info",
    )
