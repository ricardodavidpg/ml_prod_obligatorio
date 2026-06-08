from typing import List

import numpy as np
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoConfig

from src.settings import custom_logger
from src.structs.labels import ClassificationLabel
from src.structs.texts import ClassifiedText, ScoresMetadata
from src.structs.payload import TextsPayload, ResponsePropertyPayload


class Classifier:
    """Class for handling the text classification operations."""

    def __init__(self, model_id: str, batch_size: int):
        self.logger = custom_logger(self.__class__.__name__)
        self.model_id = model_id
        self.batch_size = batch_size


        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.logger.info(f"Using device: {self.device}")
        self.load_model()

    def load_model(self):
        """Method for loading the model and tokenizer from the Hugging Face model hub."""

        self.logger.info(f"Loading model {self.model_id}")
        self.model_config = AutoConfig.from_pretrained(self.model_id)
        self.num_labels = len(self.model_config.id2label)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_id, num_labels=self.num_labels
        ).to(self.device)
        self.logger.info(f"Model {self.model_id} loaded successfully!")

    def _create_batches(self, texts: List[str]):
        """
        Yield successive n-sized chunks from a list of texts.

        Args:
            texts: List of texts to create batches from

        Returns:
            Generator of batches of texts
        """
        for i in range(0, len(texts), self.batch_size):
            yield texts[i : i + self.batch_size]

    def predict(self, payload: TextsPayload) -> ResponsePropertyPayload:
        results = []
        for batch_texts in self._create_batches(payload.texts):
            # Tokenizar, pasar de texto a tensores
            encoded_input = self.tokenizer(
                batch_texts,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=self.model_config.max_position_embeddings - 2,
            ).to(self.device)

            with torch.no_grad(): #Puntajes para cada clase, se aplica softmax para obtener probabilidades
                scores = torch.softmax(self.model(**encoded_input).logits, dim=-1).cpu().numpy()

            # Estructurar el output, quedándonos con la clase de mayor puntaje, 
            # pero también guardando el puntaje de cada clase en metadata
            for i, text in enumerate(batch_texts):
                top_idx = np.argmax(scores[i])
                top_label = self.model_config.id2label[top_idx]

                results.append(ClassifiedText(
                    text=text,
                    label=ClassificationLabel(top_label),
                    score=float(scores[i][top_idx]),
                    metadata=ScoresMetadata(scores={
                        ClassificationLabel(self.model_config.id2label[j]): float(scores[i][j])
                        for j in range(self.num_labels)
                    }),
                ))

        return ResponsePropertyPayload(texts=results, model_id=self.model_id)