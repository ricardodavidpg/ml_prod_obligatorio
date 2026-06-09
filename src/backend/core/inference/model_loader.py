import os
import joblib
from pathlib import Path

ARTIFACTS_DIR = Path("artifacts")

def load_model():
    model_name = os.getenv("ACTIVE_MODEL", "model.pkl")
    model_path = ARTIFACTS_DIR / model_name

    if not model_path.exists():
        raise FileNotFoundError(f"No existe el modelo: {model_path}")

    return joblib.load(model_path)