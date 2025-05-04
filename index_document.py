from chatbot.document_indexer import DocumentIndexer

if __name__ == "__main__":
    indexer = DocumentIndexer()
    indexer.index_pdf("data/AkhilSuresh_CV.pdf")
