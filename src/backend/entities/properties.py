from enum import Enum
from pydantic import BaseModel

class PropertyType(str, Enum):
    """Represents all supported property types."""

    HOUSE = "House"
    APARTMENT = "Apartment"

    def __str__(self):
        return str(self.value)

class Property(BaseModel):
    """
    Represents the characteristics of a property.

    Attributes:
        property_type: Type of the property.
        area: Property area in square meters.
        bedrooms: Number of bedrooms.
        bathrooms: Number of bathrooms.
        neighborhood: Name of the neighborhood.   
    """
    
    property_type: PropertyType
    area: int
    bedrooms: int
    bathrooms:int
    neighborhood:str

class ClassifiedProperty(BaseModel):
    """
    Represents a property that has already been classified.

    Attributes:
        property: Original property information.
        predicted_price: Price predicted by the model.
    """

    property: Property
    predicted_price: float

