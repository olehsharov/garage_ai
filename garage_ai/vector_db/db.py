from pathlib import Path
from abc import ABC, abstractmethod
from typing import List
import faiss
import numpy as np
import sqlite3

from torch import Tensor

from garage_ai.embeddings.providers import AbstractEmbeddings
from garage_ai.ingest.pdf import PdfProcessor
from garage_ai.metadata.storage import MetadataStorage

class AbstractDb(ABC):

    def __init__(self, embedding_provider: AbstractEmbeddings, pdf_processor: PdfProcessor):
        self.embedding_provider = embedding_provider
        self.pdf_processor = pdf_processor

    def add_text(self, pdf_path:Path):
        text = self.pdf_processor.extract_text(pdf_path) + "\n"
        text += str(pdf_path)
        embeddings = self.embedding_provider.encode_embeddings([text])
        self._add_text(str(pdf_path), embeddings)

    def query_text(self, text:str) -> List[str]:
        return self._query_text(text)

    @abstractmethod
    def _add_text(self, pdf_path:str, embeddings: List[Tensor] | np.ndarray | Tensor):
        pass

    @abstractmethod
    def _query_text(self, text) -> List[str]:
        pass

class FaissDb(AbstractDb):

    def __init__(self, embedding_provider: AbstractEmbeddings, pdf_processor: PdfProcessor, index_folder:Path):
        super().__init__(embedding_provider, pdf_processor)

        index_folder = Path(index_folder)
        index_folder.mkdir(exist_ok=True, parents=True)

        db_path = Path(index_folder / "metadata.db")
        self.conn = sqlite3.connect(db_path)
        self.index_path = Path(index_folder / "faiss.index")
        self._read_index()
        self._create_table()

    def _read_index(self):
        if self.index_path.exists():
            self.index = faiss.read_index(str(self.index_path))
        else:
            self.index = faiss.IndexIDMap(faiss.IndexFlatL2(self.embedding_provider.dims()))

    def _write_index(self):
        faiss.write_index(self.index, str(self.index_path))

    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS metadata (
            id INTEGER PRIMARY KEY,
            filename TEXT
        )
        """)
        self.conn.commit()

    def _pdf_id(self, pdf_path):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM metadata WHERE filename=?", (pdf_path,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO metadata (filename) VALUES (?)", (pdf_path,))
            self.conn.commit()
        cursor.execute("SELECT id FROM metadata WHERE filename=?", (pdf_path,))
        return cursor.fetchone()[0]

    def _add_text(self, pdf_path:str, embeddings: List[Tensor] | np.ndarray | Tensor):
        pdf_id = self._pdf_id(pdf_path)
        self.index.add_with_ids(embeddings, [pdf_id])
        self._write_index()

    def _query_text(self, text:str) -> List[str]:
        embeddings = self.embedding_provider.encode_embeddings([text])
        D, I = self.index.search(embeddings, k=5)
        cursor = self.conn.cursor()
        result = []
        for i in I[0]:
            select = cursor.execute("SELECT filename FROM metadata WHERE id=?", (int(i),))
            fetched = select.fetchone()
            if fetched is not None:
                result.append(fetched[0])
        return result
                
            