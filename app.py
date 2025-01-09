import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_pdf_text(pdf_docs):
    """Extracts text from uploaded PDF files."""
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    """Splits extracted text into manageable chunks."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    """Creates and saves a FAISS vector store from text chunks."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    """Sets up a conversational chain using Flash Gemini 2.0 model."""
    prompt_template = """
    Answer the question as detailed as possible from the provided context. If the answer is not in
    the provided context, just say, "answer is not available in the context." Do not provide incorrect answers.

    Context:
    {context}?

    Question:
    {question}

    Answer:
    """
    
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question):
    """Handles user queries by retrieving answers from the vector store."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    response = chain(
        {"input_documents": docs, "question": user_question},
        return_only_outputs=True
    )

    st.markdown(f"### Reply:\n{response['output_text']}")

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title="Chat PDF", page_icon=":books:", layout="wide")
    st.title("Chat with PDF using Flash Gemini 2.0 :smile:")
    
    st.sidebar.header("Upload & Process PDF Files")
    st.sidebar.markdown(
        "Use Flash Gemini 2.0 model for advanced conversational capabilities.")
    
    with st.sidebar:
        pdf_docs = st.file_uploader(
            "Upload your PDF files:",
            accept_multiple_files=True,
            type=["pdf"]
        )
        if st.button("Submit & Process"):
            with st.spinner("Processing your files..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("PDFs processed and indexed successfully!")

    st.markdown(
        "### Ask Questions from Your PDF Files :mag:\n"
        "Once you upload and process your PDFs, type your questions below."
    )

    user_question = st.text_input("Enter your question:", placeholder="What do you want to know?")

    if user_question:
        with st.spinner("Fetching your answer..."):
            user_input(user_question)

    st.sidebar.info(
        "**Note:** This app uses the 2.0 Flash Gemini model for answering questions accurately."
    )

if __name__ == "__main__":
    main()