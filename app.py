# app.py

from flask import Flask, render_template, request, jsonify
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOllama
import os

# Import functions and prompt from your files
from src.helper import embedding_creation
from src.prompt import prompt as prompt_template # Renaming to avoid conflict

# Initialize the Flask application
app = Flask(__name__)

# --- Global Variables ---
# These will be loaded once when the app starts
retriever = None
llm = None
VECTOR_STORE_PATH = "faiss_index"

def setup_llm_and_retriever():
    """
    Loads the LLM and the pre-built FAISS index.
    """
    global retriever, llm

    # --- Setup LLM ---
    print("Loading the LLM...")
    # This now happens only once
    llm = ChatOllama(model="phi3:mini", temperature=0.2)
    print("LLM loaded.")

    # --- Setup Retriever ---
    if not os.path.exists(VECTOR_STORE_PATH):
        print(f"Error: Vector store not found at '{VECTOR_STORE_PATH}'.")
        print("Please run 'create_vector_store.py' first to create it.")
        return

    print("Loading the vector store...")
    embeddings = embedding_creation()
    
    # Load the local FAISS index
    vector_store = FAISS.load_local(
        VECTOR_STORE_PATH, 
        embeddings,
        allow_dangerous_deserialization=True 
    )
    
    retriever = vector_store.as_retriever(search_kwargs={'k': 4})
    print("Retriever is ready.")


# --- Flask Routes ---

@app.route("/")
def index():
    """Renders the main chat page."""
    return render_template('index.html')

@app.route("/get_response", methods=["POST"])
def get_response():
    """Handles the user's question and returns the chatbot's response."""
    if not retriever or not llm:
        return jsonify({"error": "Chatbot is not set up correctly. Please check server logs."})

    user_question = request.json.get("question")
    if not user_question:
        return jsonify({"error": "No question provided."})

    # Retrieve relevant documents
    retrieved_docs = retriever.invoke(user_question)
    context = "\n\n".join(doc.page_content for doc in retrieved_docs)

    # Use the imported prompt template
    final_prompt = prompt_template.invoke({'context': context, 'question': user_question})

    # Generate response using the globally loaded LLM
    response = llm.invoke(final_prompt)
    answer = response.content if hasattr(response, 'content') else str(response)

    return jsonify({"answer": answer})

# --- Main Execution ---

if __name__ == '__main__':
    # Set up the retriever and LLM when the application starts
    setup_llm_and_retriever()
    # Run the Flask app
    app.run(debug=True, port=5000)
