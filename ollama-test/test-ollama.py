from langchain_community.llms import Ollama

# Load the Ollama LLM
llm = Ollama(model="llama3.2:latest")  # Change "llama2" to your actual model name

# Take user input and generate response
user_input = input("You: ")
response = llm.invoke(user_input)
print("\nLLM:", response)