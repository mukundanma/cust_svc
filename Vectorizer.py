from typing import List
from openai import OpenAI


class Vectorizer:
    def __init__(self, client: OpenAI, model: str, dimensions: int):
        self._client = client
        self._model = model
        self._dimensions = dimensions

    def vectorize(self, chunks) -> list[List[float]]:
        vectors = [
            vec.embedding
            for vec in self._client.embeddings.create(
                input=chunks, model=self._model, dimensions=self._dimensions
            ).data
        ]
        return vectors
