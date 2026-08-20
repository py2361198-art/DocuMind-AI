import faiss
import numpy as np


class VectorStore:
    def __init__(self):
        self.index = None
        self.chunks = []

    def add(self, embeddings, chunks):
        vectors = np.array(embeddings).astype("float32")

        self.index = faiss.IndexFlatL2(vectors.shape[1])
        self.index.add(vectors)

        self.chunks = chunks

    def search(self, query_embedding, top_k=3):
        if self.index is None:
            return []

        query = np.array([query_embedding]).astype("float32")

        distances, indices = self.index.search(query, top_k)

        results = []

        for index in indices[0]:
            if index < len(self.chunks):
                results.append(self.chunks[index])

        return results
