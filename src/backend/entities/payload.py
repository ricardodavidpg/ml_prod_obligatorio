from src.entities.properties import ClassifiedProperty, Property
from typing import List
from pydantic import BaseModel

class PropertyPayload(BaseModel):
    """Input payload for the classification endpoint"""

    properties: List[Property]

class ResponsePropertyPayload(BaseModel):
    """Response payload for the classification endpoint"""

    properties: List[ClassifiedProperty]