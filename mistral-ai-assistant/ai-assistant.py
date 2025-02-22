import streamlit as st
from langchain_ollama import OllamaLLM

# Set up Streamlit UI
st.set_page_config(page_title="Mistral 7B Chatbot", layout="wide")
st.title("🤖💬 Chat with Mistral 7B (Running Locally)")

# Initialize the local Mistral model
llm = OllamaLLM(model="mistral")

# Store chat history
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
    