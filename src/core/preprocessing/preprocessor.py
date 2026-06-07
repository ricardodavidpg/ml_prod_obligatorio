from src.settings import custom_logger
from src.data_model.payload import PropertyPayload


class Preprocessor:
    """Class for handling the preprocessing operations of the property data"""

    def __init__(self) -> None:
        self.logger = custom_logger(self.__class__.__name__)

    def preprocess_properties(self, payload: PropertyPayload) -> PropertyPayload:
        """
        Method for preprocessing a batch of property data

        Args:
            payload: PropertyPayload object containing the properties to preprocess

        Returns:
            PropertyPayload object containing the preprocessed properties
        """
        return PropertyPayload(
            texts=[self.preprocess_text(text) for text in payload.texts]
        )

    def preprocess_property(self, text: str) -> str:
       # TODO: implementar el preprocesado de las propiedades
       pass

    