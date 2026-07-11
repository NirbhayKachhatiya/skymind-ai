import numpy as np
from typing import List

class LocalDeterministicEmbedder:
    def __init__(self, dimension: int = 1536) -> None:
        self.dimension: int = dimension

    def embed_query(self, text: str) -> List[float]:
        np.random.seed(sum(ord(c) for c in text) % 10000)
        vec = np.random.randn(self.dimension)
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec.tolist()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_query(text) for text in texts]