from embeddings import model
from vector_store import VectorStore


class RAGSystem:
    def __init__(self):
        self.vector_store = VectorStore()

    def add_documents(self, chunks):
        embeddings = model.encode(chunks).tolist()
        self.vector_store.add(embeddings, chunks)

    def search(self, question, top_k=3):
        question_embedding = model.encode([question])[0].tolist()

        return self.vector_store.search(
            question_embedding,
            top_k
        )
