from garage_ai.metadata.storage import MetadataStorage

meta_storage = MetadataStorage("data/test_data/autoincrement.db")
meta_storage.update_meta("file1", {"test": "gagaga"})
meta = meta_storage.get_meta("file1")
assert meta["test"] == "gagaga", "It should be gagaga"

meta_storage.update_meta("file1", {"test2": "gagaga2"})
meta = meta_storage.get_meta("file1")
assert meta["test2"] == "gagaga2", "It should be gagaga2"
