"""Preprocesamiento compartido. Lo importan tanto el entrenamiento como (después) la API,
para garantizar que los datos se preparan EXACTAMENTE igual en los dos lados (anti-skew)."""

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Regresión: predecimos el precio. Por eso 'price' es el TARGET y NO va en las features
# (usarlo como entrada para predecirlo sería leakage total).
NUMERICAS   = ["area", "bedrooms", "bathrooms"]
CATEGORICAS = ["property_type", "neighborhood"]
FEATURES    = CATEGORICAS + NUMERICAS
TARGET      = "price"

def crear_preprocesador():
    return ColumnTransformer([
        ("num", StandardScaler(), NUMERICAS),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAS),
    ])