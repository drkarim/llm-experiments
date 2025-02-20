import streamlit as st
from langchain_community.llms import Ollama

# Initialize the local Ollama model
llm = Ollama(model="llama3.2:latest")  # Ensure this model exists in `ollama list`

# Streamlit UI setup
st.set_page_config(page_title="Chat with Llama 3.2", layout="wide")
st.title("🦙💬 Chat with Llama 3.2 (Local LLM)")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = llm.invoke(user_input)
            st.markdown(response)

    # Store AI response in chat history
    st.session_state.messages.append({"role": "assistant", "content": response})