
from pathlib import Path
import signal
import json
import threading
import lmdb


class MetadataStorage:

    def __init__(self, db_path:Path):
        self.db_path = db_path
        self.env = lmdb.open(str(self.db_path), max_dbs=1)
        self.db = self.env.open_db(b"main")
        self.lock = threading.Lock()

        signal.signal(signal.SIGINT, self._close_db)
        signal.signal(signal.SIGTERM, self._close_db)

    def _close_db(self, signum, frame):
        self.env.close()

    def get_meta(self, file: str) -> dict:
        with self.lock, self.env.begin(db=self.db, write=True) as txn:
            value = txn.get(file.encode())
            if value:
                return json.loads(value.decode())

    def update_meta(self, file: str, meta:dict):
        with self.lock, self.env.begin(db=self.db, write=True) as txn:
            metadata = txn.get(file.encode())
            if metadata:
                metadata_dict = json.loads(metadata.decode())
                metadata_dict = {**metadata_dict, **meta}
                txn.put(file.encode(), json.dumps(metadata_dict).encode())
            else:
                metadata_dict = meta
                txn.put(file.encode(), json.dumps(metadata_dict).encode())

    def all(self):
        with self.lock, self.env.begin(db=self.db) as txn:
            cursor = txn.cursor()
            for key, value in cursor:
                yield key.decode(), json.loads(value.decode())