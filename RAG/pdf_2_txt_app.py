import streamlit as st
import fitz  # PyMuPDF

def extract_text_from_pdf(uploaded_file):
    """Extracts text from an uploaded PDF file."""
    try:
        # Open the PDF from the uploaded file object
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
        return text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def main():
    st.title("PDF to Text Converter")
    st.write("Upload a PDF file and extract its text content.")
    
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    
    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        
        # Extract text
        text = extract_text_from_pdf(uploaded_file)
        
        # Display extracted text
        st.subheader("Extracted Text:")
        st.text_area("", text, height=300)
        
        # Provide a download button for text file
        text_filename = uploaded_file.name.replace(".pdf", ".txt")
        st.download_button(
            label="Download Extracted Text",
            data=text,
            file_name=text_filename,
            mime="text/plain"
        )

if __name__ == "__main__":
    main()