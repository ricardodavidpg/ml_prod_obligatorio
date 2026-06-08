from src.core.preprocessing import Preprocessor
from src.structs.payload import TextsPayload


def test_preprocessor():
    """Function for testing the Preprocessor class."""
    # Create a preprocessor instance
    preprocessor = Preprocessor()

    # Define some example texts to preprocess
    texts = [
        "I'm feeling so healthy today!",
        "My day was not good, but not bad",
        "I hate when people do this",
    ]
    payload = TextsPayload(texts=texts)

    # Preprocess the texts
    preprocessed_texts: TextsPayload = preprocessor.preprocess_properties(payload)

    # Check the preprocessed texts
    assert len(preprocessed_texts.texts) == len(texts)
    assert all(isinstance(text, str) for text in preprocessed_texts.texts)
    assert all(len(text) > 0 for text in preprocessed_texts.texts)
    assert all(text.strip() == text for text in preprocessed_texts.texts)
