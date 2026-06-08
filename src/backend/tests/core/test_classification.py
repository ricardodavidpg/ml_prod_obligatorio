import pytest
from unittest.mock import patch, MagicMock
from src.core.classification import Classifier
from src.structs.payload import TextsPayload, ResponsePropertyPayload
from src.settings import SettingsManager



def test_classifier():
    """Function for testing the Classifier class."""
    # Load settings
    settings = SettingsManager()

    # Create a classifier instance
    classifier = Classifier(model_id=settings.MODEL_ID, batch_size=settings.BATCH_SIZE)

    # Define the example texts with their expected scores
    example_texts = [
        {
            "text": "I'm feeling so healthy today!",
            "expected_label": "positive",
            "expected_score_range": (0.8, 1.0),
        },
        {
            "text": "I have to study today",
            "expected_label": "neutral",
            "expected_score_range": (0.5, 0.8),
        },
        {
            "text": "I hate when people do this",
            "expected_label": "negative",
            "expected_score_range": (0.8, 1.0),
        },
    ]

    # Crea solicitud con los textos de ejemplo
    input_payload = TextsPayload(texts=[example["text"] for example in example_texts])

    preds: ResponsePropertyPayload = classifier.predict(input_payload)

    # Valida que las predicciones coincidan con los esperado
    for example, pred in zip(example_texts, preds.texts):
        text = example["text"]
        expected_label = example["expected_label"]
        expected_score_range = example["expected_score_range"]


        assert pred.label.value == expected_label

        assert expected_score_range[0] <= pred.score <= expected_score_range[1]
