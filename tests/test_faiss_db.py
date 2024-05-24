from garage_ai.ingest.pdf import PdfProcessor
from garage_ai.vector_db.db import FaissDb
from garage_ai.embeddings.providers import SentenceTransformerEmbeddings
from garage_ai.walker import Walker

db = FaissDb(
    embedding_provider=SentenceTransformerEmbeddings(), 
    pdf_processor=PdfProcessor(), 
    index_folder="tmp/faiss_test"
)
# db.add_text("data/test_data/pdfs/AB Airbag Sys.pdf")

walker = Walker("data/pages")
files = walker.walk()
total = len(files)
print("Total files:", total)
for idx, file in enumerate(files):
    print(f"[{idx}/{total}] Embedding file:", file)
    db.add_text(file)

# documents = db.query_text("forester automatic transmission oil seal")
# for doc in documents:
#     print(doc)