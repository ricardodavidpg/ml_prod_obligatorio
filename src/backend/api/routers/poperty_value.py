from fastapi import APIRouter, Request
from fastapi import Body

from src.entities.properties import ClassifiedProperty, Property, PropertyType
from src.entities.payload import PropertyPayload, ResponsePropertyPayload
from src.settings import custom_logger
from src.core.inference.inference_pipeline import predict

from typing import List

logger = custom_logger("Properties Classification Router")

properties_classification_router = APIRouter()


@properties_classification_router.post("/houses")
def classify_texts(
    request: Request, body: PropertyPayload = Body(...)
) -> ResponsePropertyPayload:
    """
    Endpoint for classifying a list of texts

    Args:
        request: Request object
        property: PropertyPayload object containing the property to classify

    Returns:
        ResponsePropertyPayload object containing the classified Property
    """
    
    model = request.state.model
    predicted_price = predict(body.properties, model)

    response = ResponsePropertyPayload(
        properties = [
            ClassifiedProperty(
                property = property, 
                predicted_price = price
            ) 
            for property, price in zip(body.properties, predicted_price)
        ]
    )
    return response
