from garage_ai.embeddings.providers import SentenceTransformerEmbeddings

embeddings_provider = SentenceTransformerEmbeddings()
embeddings = embeddings_provider.encode_embeddings("Hello, world!")
print(embeddings.shape)
print(embeddings_provider.dims())