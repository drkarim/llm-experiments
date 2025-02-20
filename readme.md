# 🦙💬 Local AI Chatbot using Ollama + LangChain + Streamlit

This repository contains Python scripts that use **Ollama**, **LangChain**, and **Streamlit** to run a local AI chatbot on **macOS Silicon (M1/M2/M3/M4)** devices.  

With these scripts, you can:  
✅ Run a **local LLM** (Large Language Model) on your Mac  
✅ Test your model with a single prompt  
✅ Build an **interactive chatbot** using Streamlit  
✅ Enable **chat memory** and **streaming responses**  
✅ Upload a **PDF file** and chat with its contents  

---

## **🔹 1. Download & Install Ollama on macOS**
Ollama lets you run **LLMs (Large Language Models) locally** on your Mac.  

### **🔽 Install Ollama**
Run the following command in your terminal:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### **📥 Download a Local LLM Model**
After installing **Ollama**, you can download a model like **Llama 3**:
```bash
ollama pull llama3:latest
```
Other models you can try:
```bash
ollama pull mistral
ollama pull gemma
```

---

## **🔹 2. Test That Your Ollama Model Works**
After downloading a model, test it with:
```bash
ollama run llama3
```
If the model responds, you're ready to move to the next step! 🎉

---

## **🔹 3. Install Required Python Libraries**
Ensure you have **Python 3.10+** installed. Then install the required libraries:
```bash
pip install streamlit langchain langchain-community langchain-ollama ollama faiss-cpu pypdf
```

---

## **🔹 4. About the Python Scripts in This Repository**
This repo contains **four scripts**, each building upon the previous one:  

### **📄 1️⃣ test-ollama.py (Basic Test)**
🔹 **Tests your Ollama model with a single user input**.  
🔹 **Simply takes a prompt and prints the model's response**.  

Run it with:
```bash
python test-ollama.py
```

---

### **📄 2️⃣ streamlit-chat.py (Basic Chatbot)**
🔹 **Creates a simple chatbot using Streamlit**.  
🔹 **Takes user input and uses the local LLM to respond**.  
🔹 **No memory or streaming output—just basic interaction**.  

Run it with:
```bash
streamlit run streamlit-chat.py
```

---

### **📄 3️⃣ ollama-llm-ai-assistant.py (Advanced Chatbot)**
🔹 **Enhances the chatbot with memory & real-time streaming output**.  
🔹 **Keeps track of conversation history**.  
🔹 **Displays responses in real-time as they are generated**.  

Run it with:
```bash
streamlit run ollama-llm-ai-assistant.py
```

---

### **📄 4️⃣ chatpdf-v1.py (Chat with a PDF)**
🔹 Allows you to upload any PDF file and ask questions based on its content.
🔹 Uses FAISS vector search to efficiently retrieve relevant document chunks.
🔹 Employs Ollama's local LLM (`llama3.2:latest`) to generate responses.
🔹 Works entirely offline for privacy and security.

#### **🔹 How to Run the PDF Chatbot**
1. Ensure you have installed all dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

2. Run the chatbot using Streamlit:
   ```bash
   streamlit run ./chatpdf/chatpdf-v1.py
   ```

3. Upload a PDF file and start chatting with it! 🚀

#### **🛠️ Special Instructions for macOS Users**
On macOS, you need to set an **environment variable** to prevent FAISS from causing OpenMP errors. Run this command before starting the chatbot:  
```bash
export KMP_DUPLICATE_LIB_OK=TRUE
```
To make this permanent, add the following lines to your **~/.zshrc** or **~/.bashrc** file:
```bash
echo 'export KMP_DUPLICATE_LIB_OK=TRUE' >> ~/.zshrc
echo 'export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES' >> ~/.zshrc
source ~/.zshrc
```
This ensures that FAISS runs smoothly on macOS. 🚀  

---

## **🔹 5. Running the Streamlit Apps**
After cloning this repository, navigate to the project folder and run:
```bash
streamlit run streamlit-chat.py
```
or
```bash
streamlit run ollama-llm-ai-assistant.py
```
or
```bash
streamlit run chatpdf-v1.py
```
This will open an interactive chatbot in your web browser. 🚀  

---

## **💡 Notes**
- Ensure you have **Ollama running** before using the scripts.
- If you want to try **different models**, update the model name in the Python scripts.
- Running **larger models** may require **more RAM and processing power**.

---

## **🤝 Contributing**
Feel free to **open an issue** or **submit a pull request** if you have improvements or bug fixes! 😊

---

## **📜 License**
This project is licensed under the **MIT License**.

---
Happy chatting! 🎙️💬🚀
