from fastapi import APIRouter, Request
from fastapi import Body

from src.entities.properties import ClassifiedProperty, Property
from src.entities.payload import PropertyRequest, PropertyResponse
from src.settings import custom_logger
from src.core.inference.inference_pipeline import predict

from typing import List

logger = custom_logger("Properties Classification Router")

properties_classification_router = APIRouter()


@properties_classification_router.post(
    "/houses",
    summary="Predecir precio de propiedades",
    response_description="Lista de propiedades con sus precios estimados.",
)
def classify_texts(
    request: Request, body: PropertyRequest = Body(...)
) -> PropertyResponse:
    """
    Recibe una lista de propiedades y retorna el precio estimado para cada una.

    Barrios soportados: Aguada, Aires Puros, Arroyo Seco, Atahualpa, Barra de Carrasco,
    Barrio Lagos de Carrasco, Barrio Parques, Barrio San Nicolás, Barrio Sur,
    Bañados de Carrasco, Bella Italia, Bella Vista, Belvedere, Bolivar, Brazo Oriental,
    Buceo, Camino Maldonado, Capurro, Capurro Bella Vista, Carrasco,
    Carrasco Barrios con Seguridad, Carrasco Este, Carrasco Norte, Casabo Pajas Blancas,
    Casavalle, Centro, Cerrito, Cerro, Ciudad Vieja, Colón, Conciliación, Cordón,
    Flor de Maroñas, Goes, Golf, Ituzaingó, Jacinto Vera, Jardines de Carrasco,
    Jardines del Hipódromo, La Blanqueada, La Comercial, La Figurita,
    La Paloma Tomkinson, La Teja, Larrañaga, Las Acacias, Las Canteras, Lezica,
    Los Olivos, Malvín, Malvín Norte, Manga, Marconi, Maroñas, Melilla,
    Mercado Modelo, Montevideo, Nuevo París, Pajas Blancas, Palermo, Parque Batlle,
    Parque Miramar, Parque Rodó, Paso Molino, Paso de la Arena, Perez Castellanos,
    Peñarol, Peñarol Lavalleja, Piedras Blancas, Pocitos, Pocitos Nuevo, Prado,
    Prado Nueva Savona, Puerto Buceo, Punta Carretas, Punta Gorda, Punta Rieles,
    Reducto, Sayago, Tres Cruces, Tres Ombues Pblo Victoria, Unión, Villa Biarritz,
    Villa Dolores, Villa Española, Villa García Manga Rural, Villa Muñoz, Zona Rural.
    """
    
    model = request.state.model
    predicted_price = predict(body.properties, model)

    response = PropertyResponse(
        properties = [
            ClassifiedProperty(
                property = property, 
                predicted_price = price
            ) 
            for property, price in zip(body.properties, predicted_price)
        ]
    )
    return response
