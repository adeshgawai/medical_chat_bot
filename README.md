🩺 Medical Document Chatbot

This project is a sophisticated, locally-run medical chatbot that leverages a Retrieval-Augmented Generation (RAG) architecture. It allows users to ask questions about a collection of medical documents (PDFs) and receive accurate, context-aware answers through a user-friendly web interface.

The application uses a local LLM via Ollama for inference while leveraging Pinecone (cloud-based vector database) for document retrieval. This ensures scalable and efficient similarity search while still keeping sensitive LLM inference local.

✨ Features

Hybrid Setup: Inference happens locally with Ollama, while embeddings are stored and queried using Pinecone.

RAG Architecture: Retrieves relevant document chunks from Pinecone before generating responses.

PDF Data Source: Easily ingest your own collection of medical PDFs.

Pinecone Vector Database: Provides fast, cloud-hosted similarity search for large document collections.

Web Interface: Clean and responsive interface built with Flask.

Dark Mode: Includes a theme toggler with saved preferences.

📂 Project Structure:
medical_chatbot/
│
├── app.py                  # Main Flask application
├── create_vector_store.py  # Script to upload document embeddings to Pinecone
├── helper.py               # Helper functions (PDF parsing, embeddings, etc.)
├── prompt.py               # Prompt template for the LLM
├── requirements.txt        # Project dependencies
│
├── data/                   # Store your PDF documents here
│   ├── medical_doc_1.pdf
│   └── ...
│
├── templates/              # Frontend templates
│   └── index.html
│
└── static/                 # Static assets (CSS, JS, images)
    └── style.css
⚙️ Setup and Installation
Prerequisites

Python 3.8+

Ollama installed and running

phi3:mini model pulled via Ollama:
Pinecone account and API key

Installation

Clone the repository (or set up your project folder).

Create a virtual environment (recommended):

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate


Install dependencies:
Create a requirements.txt file with the following:

Flask
langchain
langchain-community
pinecone-client
sentence-transformers
pypdf


Then install:

pip install -r requirements.txt


Set up environment variables:
Create a .env file in the root directory with:

PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_env
PINECONE_INDEX=medical-chatbot-index

🚀 How to Run
Step 1: Upload Documents to Pinecone

Place your PDF files in the /data directory.

Run the ingestion script to create embeddings and push them to Pinecone:

python create_vector_store.py

Step 2: Start the Chatbot Application

Make sure Ollama is running in the background.

Start the Flask app:

python app.py


Open your browser and visit:

http://127.0.0.1:5000


You can now chat with your medical documents!

🛠️ Technologies Used

Backend: Flask

Machine Learning: LangChain, PyTorch

LLM: Ollama (phi3:mini)

Vector Database: Pinecone (cloud-based)

Embeddings: Sentence-Transformers (all-MiniLM-L6-v2)

Frontend: HTML, CSS, JavaScript