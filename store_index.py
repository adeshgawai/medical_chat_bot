# create_vector_store.py

from src.helper import load_pdf_file, text_spltter, embedding_creation
from langchain_community.vectorstores import FAISS
import os

# Define the path for the persistent vector store
VECTOR_STORE_PATH = "faiss_index"
DATA_PATH = "data/"

def main():
    """
    Main function to create and save the FAISS vector store.
    """
    print("Starting to create the vector store...")

    # Load documents
    print(f"Loading documents from {DATA_PATH}...")
    extracted_docs = load_pdf_file(DATA_PATH)
    if not extracted_docs:
        print("No documents found. Exiting.")
        return
    print(f"Loaded {len(extracted_docs)} documents.")

    # Split documents into chunks
    print("Splitting documents...")
    text_chunks = text_spltter(extracted_docs)
    print(f"Created {len(text_chunks)} text chunks.")

    # Create embeddings
    print("Creating embeddings...")
    embeddings = embedding_creation()

    # Create and save the FAISS vector store
    print(f"Creating and saving the vector store to {VECTOR_STORE_PATH}...")
    vector_store = FAISS.from_documents(text_chunks, embeddings)
    vector_store.save_local(VECTOR_STORE_PATH)

    print("Vector store created and saved successfully!")

if __name__ == "__main__":
    main()
