import os
import fitz
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

class DocumentIndexer:
    def __init__(self, index_dir="doc_index", model_name="all-MiniLM-L6-v2"):
        self.index_dir = index_dir
        self.embedding_model = SentenceTransformer(model_name)
        self.index_file = os.path.join(index_dir, "faiss.index")
        self.meta_file = os.path.join(index_dir, "metadata.pkl")
        os.makedirs(index_dir, exist_ok=True)

    def extract_text(self, file_path):
        doc = fitz.open(file_path)
        return " ".join([page.get_text() for page in doc])

    def chunk_text(self, text, chunk_size=500):
        words = text.split()
        return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

    def embed_chunks(self, chunks):
        return self.embedding_model.encode(chunks, convert_to_tensor=False)

    def save_index(self, embeddings, chunks, doc_name):
        if os.path.exists(self.index_file) and os.path.exists(self.meta_file):
            index = faiss.read_index(self.index_file)
            with open(self.meta_file, 'rb') as f:
                metadata = pickle.load(f)
        else:
            index = faiss.IndexFlatL2(self.embedding_model.get_sentence_embedding_dimension())
            metadata = []

        index.add(np.array(embeddings).astype("float32"))
        metadata.extend({"doc_name": doc_name, "text": chunk} for chunk in chunks)

        faiss.write_index(index, self.index_file)
        with open(self.meta_file, 'wb') as f:
            pickle.dump(metadata, f)

    def index_pdf(self, file_path):
        text = self.extract_text(file_path)
        if not text.strip():
            print(f"⚠️ No extractable text in {file_path}")
            return
        chunks = self.chunk_text(text)
        embeddings = self.embed_chunks(chunks)
        self.save_index(embeddings, chunks, os.path.basename(file_path))
        print(f"✅ Indexed {file_path} with {len(chunks)} chunks")
