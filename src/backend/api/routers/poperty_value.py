from fastapi import APIRouter, Request
from fastapi import Body

from src.data_model.properties import ClassifiedProperty, Property, PropertyType
from src.data_model.payload import PropertyPayload, ResponsePropertyPayload
from src.settings import custom_logger



from typing import List


logger = custom_logger("Properties Classification Router")

properties_classification_router = APIRouter()


@properties_classification_router.post("/houses")
def classify_texts(
    request: Request, property: PropertyPayload = Body(...)
) -> ResponsePropertyPayload:
    """
    Endpoint for classifying a list of texts

    Args:
        request: Request object
        property: PropertyPayload object containing the property to classify

    Returns:
        ResponsePropertyPayload object containing the classified Property
    """

    # TODO: Definir llamado al preprocesador y al clasificador una vez los tengamos implementados
    # Momentaneeamente se deja una response dummy
    """  preprocessed_payload: PropertyPayload = request.state.preprocessor.preprocess_texts(
        property
    )
    response: ResponsePropertyPayload = request.state.classifier.predict(
        preprocessed_payload
    )"""

    response = ResponsePropertyPayload(
        properties=[
            ClassifiedProperty(
                property=item.property,
                predicted_price=item.property.area * 1500,
                rating=(
                    "Overpriced"
                    if item.owner_price > item.property.area * 1500 * 1.1
                    else "Underpriced"
                    if item.owner_price < item.property.area * 1500 * 0.9
                    else "Fairly priced"
                ),
            )
            for item in property.properties
        ]
    )
    return response
