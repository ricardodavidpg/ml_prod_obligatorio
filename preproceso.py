"""Preprocesamiento compartido. Lo importan tanto el entrenamiento como (después) la API,
para garantizar que los datos se preparan EXACTAMENTE igual en los dos lados (anti-skew)."""

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder

NUMERICAS   = ["metros", "dormitorios", "banos", "precio"]
CATEGORICAS = ["barrio", "tipo"]
FEATURES    = NUMERICAS + CATEGORICAS

# Barrios con menos de UMBRAL_BARRIO propiedades se mandan a "otros". 
# Se aprende con train (anti-leakage) y vive dentro del Pipeline (anti-skew). 
UMBRAL_BARRIO = 5
OTROS = "otros"

# solo train
def barrios_frecuentes(barrios, umbral=UMBRAL_BARRIO):
    """Barrios que aparecen >= umbral veces"""
    vc = pd.Series(list(barrios)).value_counts()
    return sorted(vc[vc >= umbral].index)

# train, test, API
def agrupar_barrios(barrios, frecuentes):
    """Manda a 'otros' los barrios que no están en la lista de frecuentes."""
    s = pd.Series(list(barrios))
    return s.where(s.isin(frecuentes), OTROS)

class AgrupadorBarrios(BaseEstimator, TransformerMixin):
    """Aprende los barrios frecuentes en fit (train) y manda el resto a 'otros' en transform.

    Va DENTRO del Pipeline: se serializa con el modelo, así la API agrupa los barrios
    exactamente igual que el entrenamiento (anti-skew). Los barrios nuevos no vistos
    caen en 'otros' de forma natural.
    """

    def __init__(self, umbral=UMBRAL_BARRIO, columna="barrio"):
        self.umbral = umbral
        self.columna = columna

    def fit(self, X, y=None):
        self.frecuentes_ = barrios_frecuentes(X[self.columna], self.umbral)
        self.feature_names_in_ = list(X.columns)   # recordar las columnas de entrada
        return self

    def transform(self, X):
        X = X.copy()
        X[self.columna] = agrupar_barrios(X[self.columna], self.frecuentes_).values
        return X

    def get_feature_names_out(self, input_features=None):
        return np.asarray(input_features if input_features is not None
                        else self.feature_names_in_, dtype=object)

def crear_preprocesador():
    """
    Pipeline: agrupa barrios raros en 'otros' -> escala numéricas + one-hot categóricas.
    """
    columnas = ColumnTransformer([
        ("num", StandardScaler(), NUMERICAS),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAS),
    ])

    return Pipeline([
        ("agrupar_barrios", AgrupadorBarrios()),
        ("columnas", columnas),
    ])
