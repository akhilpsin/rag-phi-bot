import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer

class DocumentRetriever:
    def __init__(self, index_dir="doc_index", model_name="all-MiniLM-L6-v2"):
        self.embedding_model = SentenceTransformer(model_name)
        self.index_file = os.path.join(index_dir, "faiss.index")
        self.meta_file = os.path.join(index_dir, "metadata.pkl")
        self.index = None
        self.metadata = []

        self._load_index()

    def _load_index(self):
        if os.path.exists(self.index_file) and os.path.exists(self.meta_file):
            self.index = faiss.read_index(self.index_file)
            with open(self.meta_file, "rb") as f:
                self.metadata = pickle.load(f)
            print("📄 Document index loaded successfully.")
        else:
            print("⚠️ FAISS index or metadata not found.")

    def retrieve(self, query, top_k=2):
        if not self.index:
            return []
        query_embedding = self.embedding_model.encode([query])
        distances, indices = self.index.search(query_embedding, top_k)
        return [self.metadata[i]["text"] for i in indices[0] if i != -1]
