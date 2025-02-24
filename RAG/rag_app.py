import streamlit as st
import os
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.llms import Ollama
from langchain.chains import RetrievalQA

# Set up paths
FAISS_INDEX_PATH = "faiss_index"

# Initialize Ollama embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Function to load or create FAISS index
def load_vectorstore():
    if os.path.exists(FAISS_INDEX_PATH):
        return FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    return None

# Function to process and store document embeddings
def process_document(uploaded_file):
    text = uploaded_file.getvalue().decode("utf-8")

    # Split document into smaller chunks
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.create_documents([text])

    # Store in FAISS
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(FAISS_INDEX_PATH)
    return vectorstore

# Streamlit UI
st.title("RAG-Powered Document Query with Ollama")
st.write("Upload a document and ask questions.")

# File Upload
uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

# Load or process document
vectorstore = load_vectorstore()

if uploaded_file:
    st.write("Processing document...")
    vectorstore = process_document(uploaded_file)
    st.success("Document processed and indexed!")

# Ensure vectorstore is available before querying
if vectorstore:
    llm = Ollama(model="llama3.2:latest")
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever())

    # User Query Input
    query = st.text_input("Enter your query:")
    if query:
        retrieved_docs = vectorstore.similarity_search(query, k=3)

        st.subheader("Retrieved Chunks:")
        for i, doc in enumerate(retrieved_docs):
            st.write(f"**Chunk {i+1}:**")
            st.write(doc.page_content)
            st.write("---")

        # Generate response with LLM
        response = qa_chain.run(query)
        st.subheader("LLM Response:")
        st.write(response)
else:
    st.warning("Upload a document to start querying.")