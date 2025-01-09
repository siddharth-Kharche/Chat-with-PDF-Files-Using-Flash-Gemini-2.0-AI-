# Chat with PDF using Flash Gemini 2.0

This is a Streamlit-based application that allows users to interact with PDF documents by asking questions based on the content within them. The app uses the Flash Gemini 2.0 model for advanced conversational capabilities, providing users with relevant answers from the uploaded PDFs.

## Features
- Upload and process multiple PDF files.
- Extract text from PDFs and split it into manageable chunks.
- Store the extracted text in a FAISS vector store for efficient searching.
- Use the Flash Gemini 2.0 model to answer user queries based on the contents of the PDFs.
- A user-friendly interface to interact with the PDFs and get answers to your questions.

## Requirements
- Python 3.x
- Streamlit
- PyPDF2
- LangChain
- Google Generative AI
- FAISS
- dotenv

You can install the necessary libraries by running:

```bash
pip install streamlit pypdf2 langchain google-generativeai faiss-cpu dotenv
```

## Setup Instructions

1. **Clone the repository**:
   Clone this repository to your local machine or server.

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Create a `.env` file**:
   Add your Google API key to the `.env` file.

   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

3. **Run the Streamlit app**:
   After installing the required libraries and setting up the `.env` file, run the app using:

   ```bash
   streamlit run app.py
   ```

4. **Upload PDFs**:
   Once the app is running, go to the sidebar and upload one or more PDF files. After uploading, click "Submit & Process" to extract and index the text.

5. **Ask Questions**:
   After processing, you can type in questions related to the content of the uploaded PDFs. The app will fetch the relevant answer from the indexed content.

## How It Works

### PDF Text Extraction
The app uses the `PdfReader` class from the PyPDF2 library to extract text from uploaded PDF files. The extracted text is then split into smaller chunks using the `RecursiveCharacterTextSplitter` from LangChain to ensure the model can efficiently process the content.

### Vector Store
After splitting the text, the app creates a FAISS vector store using the `GoogleGenerativeAIEmbeddings` from LangChain. This vector store enables efficient similarity searches to find the most relevant text passages based on user queries.

### Question Answering
The app uses the Flash Gemini 2.0 model via the LangChain `ChatGoogleGenerativeAI` class to answer user questions based on the indexed PDF content. The question-answering chain is set up using LangChain's `load_qa_chain` method with a custom prompt template.

### Environment Configuration
Ensure that the Google API key is loaded correctly from the `.env` file using the `dotenv` library. This key is required to use the Google Generative AI model for embedding and question answering.

## Example Usage

1. Upload your PDF documents via the sidebar.
2. Click "Submit & Process" to process the documents.
3. Once the PDFs are processed, enter a question in the text input field.
4. The app will display the answer based on the content extracted from the PDFs.

## Technologies Used
- **Streamlit**: For building the web app interface.
- **PyPDF2**: For extracting text from PDF files.
- **LangChain**: For text splitting, embeddings, and question-answering functionality.
- **FAISS**: For storing and searching through text embeddings.
- **Google Generative AI**: For embedding generation and question answering.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
- Thanks to the developers of Streamlit, LangChain, FAISS, and Google Generative AI for their tools and libraries that made this app possible.
