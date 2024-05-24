from garage_ai.walker import Walker

walker = Walker("data/fsm")
files = walker.walk()
for file in files:
    meta = walker.metadata(file)
    if meta["processed"]:
        print(f"Skipping {file}")
        # walker.set_metadata(file, "processed", False)
    else:
        print(f"Processing {file}")
        walker.set_metadata(file, "processed", True)
