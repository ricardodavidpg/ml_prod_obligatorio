from src.entities.properties import ClassifiedProperty, Property
from typing import List
from pydantic import BaseModel, Field


class PropertyRequest(BaseModel):
    properties: List[Property] = Field(
        ...,
        description="Lista de propiedades a evaluar.",
        min_length=1,
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "properties": [
                        {
                            "area": 120,
                            "bedrooms": 3,
                            "bathrooms": 2,
                            "neighborhood": "Pocitos",
                        }
                    ]
                }
            ]
        }
    }


class PropertyResponse(BaseModel):
    properties: List[ClassifiedProperty] = Field(
        ...,
        description="Lista de propiedades con sus precios estimados.",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "properties": [
                        {
                            "property": {
                                "area": 120,
                                "bedrooms": 3,
                                "bathrooms": 2,
                                "neighborhood": "Pocitos",
                            },
                            "predicted_price": 185000.0,
                        }
                    ]
                }
            ]
        }
    }