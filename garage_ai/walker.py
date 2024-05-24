import lmdb
import json
from pathlib import Path
from typing import List
import threading
import signal

from garage_ai.metadata.storage import MetadataStorage

class Walker:

    def __init__(self, root: Path, verbose: bool = False):
        self.root = Path(root)
        self.verbose = verbose
        self.meta_storage = MetadataStorage("db.lmdb")

    def _meta(self, file: str):
        return {"file": file, "processed": False}

    def walk(self) -> List[Path]:
        return [str(file) for file in self.root.rglob("**/*.pdf")]

    def metadata(self, file: str) -> dict:
        return self.meta_storage.metadata(file, self._meta(file))

    def set_metadata(self, file: str, key: str, value: str):
        self.set_metadata(file, key, value)
