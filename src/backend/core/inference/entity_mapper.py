import pandas as pd
from src.entities.properties import Property
from typing import List

FEATURE_COLUMNS = [
    "property_type",
    "area",
    "bedrooms",
    "bathrooms",
    "neighborhood"
]

def property_to_dataframe(property: Property) -> pd.DataFrame:
    return {
        "property_type": property.property_type,
        "bedrooms": property.bedrooms,
        "bathrooms": property.bathrooms,
        "area": property.area,
        "neighborhood": property.neighborhood
    }

def properties_to_dataframe(properties:List[Property]):
    rows = [property_to_dataframe(p) for p in properties]
    return pd.DataFrame(rows)