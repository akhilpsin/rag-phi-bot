# 🧠 Phi RAG Chatbot

A lightweight Retrieval-Augmented Generation (RAG) chatbot that uses Ollama's **Phi** model with a custom document index to provide context-aware answers. Built with modularity, scalability, and simplicity in mind.

---

## 📂 Project Structure

```

rag-phi-bot/
├── chatbot/
│   ├── chatbot.py          # Main chatbot loop and chat logic
│   ├── phi_interface.py    # Stream interface for Ollama's Phi model
│   ├── document_indexer.py # PDF parser, chunker, embedder, FAISS indexer
│   ├── retriever.py        # Loads index, retrieves top-matching chunks
│   └── utils.py            # Hallucination filter, keyword loader
├── data/
│   └── AkhilSuresh_CV.pdf  # Example PDF to index
├── doc_index/              # Auto-generated FAISS index & metadata
│   └── faiss.index
│   └── metadata.pkl
├── hallucination_keywords.txt # Optional custom hallucination keywords
├── run_chat.py             # Chat CLI entry point
├── index_document.py       # Script to index a new PDF
├── requirements.txt
└── README.md

```

---

## 🚀 Features

- 🔎 **RAG-based responses**: Embeds and indexes PDF text for retrieval.
- 💬 **Streaming chat**: Real-time streaming replies using Ollama’s `phi` model.
- 📄 **PDF Support**: Upload your own documents for indexing.
- 🧠 **Hallucination Guard**: Auto-aborts hallucinated responses using keyword detection.
- 🧱 **Modular Design**: Easily extensible and maintainable codebase.

---

## 🛠️ Installation

1. **Install Ollama** and run the Phi model:

   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama run phi
   ```

2. **Clone and set up this repo**:

   ```bash
   git clone "https://github.com/akhilpsin/rag-phi-bot.git"
   cd rag-phi-bot
   pip install -r requirements.txt
   ```

3. **Index your documents**:

   Place your PDF in the `data/` folder, then run :

   ```bash
   python index_document.py
   ```

4. **Start chatting**:

   ```bash
   python run_chat.py
   ```

---

## 📦 Dependencies

Install via:

```bash
pip install -r requirements.txt
```

**Key Libraries:**

- `faiss-cpu`
- `sentence-transformers`
- `PyMuPDF` (`fitz`)
- `ollama`
- `aiofiles`
- `numpy`, `pickle`

---

## Output Screenshots

### 1. With Document Mode ON

When **Document Mode** is enabled, the chatbot retrieves and uses relevant documents to provide more accurate answers. Here is how the chatbot behaves with this feature enabled:

![Document Mode ON](https://github.com/akhilpsin/rag-phi-bot/Screenshot/Screenshot_DocMode_ON.jpg)

### 2. With Document Mode OFF

When **Document Mode** is disabled, the chatbot relies only on its internal knowledge base to answer the questions. Here is how the chatbot behaves without this feature:

![Document Mode OFF](https://github.com/akhilpsin/rag-phi-bot/Screenshot/Screenshot_DocMode_OFF.jpg)

---

### Instructions:

- Ensure that you have enabled the proper mode when starting the chatbot (`Y` for Document Mode ON, `N` for Document Mode OFF).
- Check the output screenshots to see the difference in how the bot answers with or without using documents.

## 📌 Notes

- To customize hallucination filtering, edit `hallucination_keywords.txt`.
- Embeddings are generated using [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) from SentenceTransformers.
- Only English-language PDFs are supported for now.
