import streamlit as st
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# Initialize the local Ollama model
llm = Ollama(model="llama3.2:latest")  # Ensure this matches your Ollama model

# Define a prompt template to maintain conversation context
prompt = PromptTemplate(
    input_variables=["history", "user_input"],
    template="You are a helpful AI assistant. Here is the conversation history:\n{history}\nUser: {user_input}\nAssistant:"
)

# Streamlit UI setup
st.set_page_config(page_title="Chat with Llama 3.2", layout="wide")
st.title("🦙💬 Chat with Llama 3.2 (Local LLM)")

# Initialize session state for chat history and memory
if "messages" not in st.session_state:
    st.session_state.messages = []
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="history", return_messages=True)

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

    # Add user input to memory
    st.session_state.memory.chat_memory.add_user_message(user_input)

    # Generate AI response with streaming
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_container = st.empty()  # Placeholder for real-time output
            response_text = ""

            # Stream response directly from Ollama
            for chunk in llm.stream(user_input):
                response_text += chunk  # Directly append the streamed text
                response_container.markdown(response_text)  # Update UI dynamically

            # Save final AI response to memory
            st.session_state.memory.chat_memory.add_ai_message(response_text)

    # Store AI response in chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text})