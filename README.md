Medical Document Chatbot
This project is a sophisticated, locally-run medical chatbot that leverages a Retrieval-Augmented Generation (RAG) architecture. It allows users to ask questions about a collection of medical documents (PDFs) and receive accurate, context-aware answers through a user-friendly web interface.

The application uses a local LLM via Ollama, ensuring that all data processing and inference happen on your machine, which is ideal for handling sensitive medical information securely.

✨ Features
Local First: All components, from the language model (Ollama's Phi-3) to the vector database (FAISS), run locally. No external API keys or internet connection are required for the core functionality.

RAG Architecture: Provides accurate answers by retrieving relevant information directly from your source documents before generating a response.

PDF Data Source: Easily ingest your own collection of medical PDF documents.

Efficient Vector Store: The application pre-processes documents into a FAISS vector store, which is saved locally. The web app loads this pre-built index for fast startup and efficient querying.

Web Interface: A clean and responsive user interface built with Flask.

Dark Mode: Includes a theme toggler for user comfort, with the preference saved in the browser.

📂 Project Structure
/medical_chatbot/
|
|-- app.py                  # Main Flask application file
|-- create_vector_store.py  # Script to create the FAISS index
|-- helper.py               # Helper functions for data processing
|-- prompt.py               # Contains the prompt template for the LLM
|-- requirements.txt        # Project dependencies
|
|-- /data/
|   |-- medical_doc_1.pdf   # <-- Place your PDF files here
|   |-- ...
|
|-- /faiss_index/           # <-- Created automatically by create_vector_store.py
|
|-- /templates/
|   |-- index.html          # Front-end HTML file
|
|-- /static/
    |-- style.css           # CSS for styling the web interface

⚙️ Setup and Installation
Follow these steps to set up and run the project on your local machine.

Prerequisites
Python 3.8+

Ollama installed and running.

The phi3:mini model pulled from Ollama. Run this command in your terminal:

ollama pull phi3:mini

Installation
Clone the repository (or set up your project folder):
Make sure you have all the project files in the structure shown above.

Create a virtual environment (recommended):

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install the required dependencies:
Create a requirements.txt file with the following content:

Flask
langchain
langchain-community
faiss-cpu
sentence-transformers
pypdf

Then, install the packages using pip:

pip install -r requirements.txt

🚀 How to Run
The application runs in a two-step process.

Step 1: Create the Vector Database
First, you need to process your PDF documents and create the local FAISS vector store.

Place all your medical PDF files inside the /data directory.

Run the create_vector_store.py script from your terminal:

python create_vector_store.py

This will create a /faiss_index folder containing your vector database. You only need to run this step once, or whenever you add or change your PDF documents.

Step 2: Start the Chatbot Application
Once the vector store is created, you can start the web server.

Make sure your Ollama application is running in the background.

Run the app.py script:

python app.py

Open your web browser and navigate to:
https://www.google.com/search?q=http://127.0.0.1:5000

You can now start asking questions through the web interface!

🛠️ Technologies Used
Backend: Flask

Machine Learning: LangChain, PyTorch

LLM: Ollama (with phi3:mini)

Vector Database: FAISS (Facebook AI Similarity Search)

Embeddings: Sentence-Transformers (all-MiniLM-L6-v2)

Frontend: HTML, CSS, JavaScript
