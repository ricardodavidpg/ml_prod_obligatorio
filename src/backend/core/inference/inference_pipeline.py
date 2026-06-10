from src.entities.properties import Property
from typing import List
from src.core.inference.entity_mapper import properties_to_dataframe
from src.core.inference.model_loader import load_model

def predict(properties:List[Property], model):
    df = properties_to_dataframe(properties)
    return model.predict(df)
