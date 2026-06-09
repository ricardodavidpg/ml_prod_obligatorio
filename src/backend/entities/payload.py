from src.data_model.properties import ToClassifyProperty, ClassifiedProperty
from typing import List
from pydantic import BaseModel

class PropertyPayload(BaseModel):
    """Input payload for the classification endpoint"""

    properties: List[ToClassifyProperty]

class ResponsePropertyPayload(BaseModel):
    """Response payload for the classification endpoint"""

    properties: List[ClassifiedProperty]