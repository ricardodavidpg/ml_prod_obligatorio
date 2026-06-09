import pandas as pd
from src.backend.entities.properties import Property

FEATURE_COLUMNS = [
    "property_type",
    "area",
    "bedrooms",
    "bathrooms",
    "neighborhood"
]

def property_to_dataframe(property: Property) -> pd.DataFrame:
    row = {
        "property_type": property.property_type,
        "bedrooms": property.bedrooms,
        "bathrooms": property.bathrooms,
        "area": property.area,
        "neighborhood": property.neighborhood
    }
    return pd.DataFrame([row], columns=FEATURE_COLUMNS)