import os
import glob
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from src.config import DATA_DIR, CHROMA_DB_DIR, EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP

def get_embeddings():
    """Returns the local HuggingFace embedding model."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

def ingest_documents():
    """Reads all PDFs and Texts in the data directory and ingests into Chroma."""
    print(f"Scanning directory for documents: {DATA_DIR}")
    pdf_files = glob.glob(os.path.join(DATA_DIR, "*.pdf"))
    txt_files = glob.glob(os.path.join(DATA_DIR, "*.txt"))
    all_files = pdf_files + txt_files

    if not all_files:
        print("No documents found to ingest.")
        return None

    documents = []
    for file_path in all_files:
        print(f"Loading {file_path}")
        if file_path.endswith(".pdf"):
            loader = PyMuPDFLoader(file_path)
            documents.extend(loader.load())
        elif file_path.endswith(".txt"):
            loader = TextLoader(file_path, encoding='utf-8')
            documents.extend(loader.load())

    print(f"Loaded {len(documents)} document pages/sections.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")

    print("Generating embeddings and storing in Chroma...")
    embeddings = get_embeddings()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_DIR
    )
    print("Ingestion complete.")
    return vectorstore

def get_retriever():
    """Returns the vector store retriever."""
    embeddings = get_embeddings()
    vectorstore = Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=embeddings
    )
    return vectorstore.as_retriever(search_kwargs={"k": 5})

if __name__ == "__main__":
    ingest_documents()
