
from abc import ABC
from typing import List

from numpy import ndarray
from torch import Tensor

class AbstractEmbeddings(ABC):

    def encode_embeddings(self, data:str) -> (List[Tensor] | ndarray | Tensor):
        pass


from sentence_transformers import SentenceTransformer

class SentenceTransformerEmbeddings(AbstractEmbeddings):

    def __init__(self, model_name:str = "sentence-transformers/all-MiniLM-L6-v2", device:str = "cuda"):
        self.model = SentenceTransformer(model_name, device=device)

    def encode_embeddings(self, data) -> (List[Tensor] | ndarray | Tensor):
        return self.model.encode(data)
    
    def dims(self) -> int:
        return self.model.get_sentence_embedding_dimension()

