import streamlit as st
import tempfile
from langchain_ollama import OllamaLLM, OllamaEmbeddings  # ✅ Updated imports
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Initialize Streamlit app
st.set_page_config(page_title="Chat with Your PDF", layout="wide")
st.title("📄🤖 Chat with Your PDF using Local LLM")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    with st.spinner("Processing the PDF..."):
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(uploaded_file.read())  # Write file contents
            temp_pdf_path = temp_pdf.name  # Get file path

        # Load PDF and extract text
        pdf_loader = PyPDFLoader(temp_pdf_path)
        pages = pdf_loader.load()

        if not pages:
            st.error("❌ No text could be extracted from the PDF. Try another file.")
            st.stop()

        # Split text into smaller chunks for better search
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        docs = text_splitter.split_documents(pages)

        if not docs:
            st.error("❌ Text splitting failed. No valid document chunks found.")
            st.stop()

        # Debugging: Show number of chunks created
        st.sidebar.write(f"🔹 Processed {len(docs)} document chunks.")

        # Create vector store (FAISS) for efficient retrieval
        embeddings = OllamaEmbeddings(model="llama3.2:latest")
        vector_store = FAISS.from_documents(docs, embeddings)

        # Create Retrieval-based QA system
        retriever = vector_store.as_retriever()

        # Define a better prompt template for retrieval-based QA
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="You are a helpful assistant. Use the following extracted context from a document to answer the question.\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"
        )

        llm = OllamaLLM(model="llama3.2:latest")  # ✅ Fixed LLM initialization
        qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

        st.success("✅ PDF uploaded and processed! You can now ask questions.")

    # Store chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    user_input = st.chat_input("Ask a question based on the PDF...")

    if user_input:
        # Display user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Retrieve relevant document chunks (Fixed: `invoke()` instead of `get_relevant_documents()`)
        retrieved_docs = retriever.invoke(user_input)

        if not retrieved_docs:
            st.warning("🤔 No relevant content found in the PDF for this question.")
        else:
            with st.expander("🔍 Retrieved Context", expanded=False):
                for doc in retrieved_docs:
                    st.write(doc.page_content[:500])  # Show first 500 characters

            # Generate AI response
            with st.chat_message("assistant"):
                with st.spinner("Searching the document..."):
                    response = qa_chain.run(user_input)
                    st.markdown(response)

            # Store AI response in chat history
            st.session_state.messages.append({"role": "assistant", "content": response})