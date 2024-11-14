import chromadb
from chromadb.config import Settings
import PyPDF2
from docx import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
import hashlib
import config
import io
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DocumentProcessor:
    def __init__(self):
        # Initialize Azure OpenAI
        self.llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version='2024-02-15-preview',
            model=os.getenv("AZURE_DEPLOYMENT_NAME"),
        )
        
        self.embeddings = AzureOpenAIEmbeddings(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_deployment=os.getenv("DEPLOYMENT_NAME", "text_embed"),
            azure_endpoint=os.getenv("ENDPOINT_URL", "https://trainee-akshay.openai.azure.com/"),
            api_version = "2024-05-01-preview",
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        # Initialize ChromaDB
        self.vectorstore = Chroma(
            persist_directory=config.CHROMA_PERSIST_DIRECTORY,
            embedding_function=self.embeddings
        )

    def extract_text(self, file, file_type):
        """Extract text from different file types."""
        if file_type == "txt":
            return file.read().decode('utf-8')
        
        elif file_type == "pdf":
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            return " ".join(page.extract_text() for page in pdf_reader.pages)
        
        elif file_type == "docx":
            doc = Document(io.BytesIO(file.read()))
            return " ".join(paragraph.text for paragraph in doc.paragraphs)
        
        raise ValueError(f"Unsupported file type: {file_type}")

    def preprocess_text(self, text):
        """Clean and preprocess the text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Remove special characters
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        return text

    def get_document_chunks(self, text):
        """Split document into chunks."""
        return self.text_splitter.split_text(text)

    def store_document(self, chunks, doc_id):
        """Store document chunks in vector store."""
        texts = [chunk for chunk in chunks]
        metadatas = [{"doc_id": doc_id, "chunk_index": i} for i in range(len(chunks))]
        
        self.vectorstore.add_texts(
            texts=texts,
            metadatas=metadatas
        )

    def compare_documents(self, doc1_id, doc2_id, query=None):
        """Compare two documents using RAG."""
        # Default comparison query if none provided
        if not query:
            query = "Compare the main ideas, similarities, and differences between the documents"

        # Retrieve relevant chunks from both documents
        search_results = self.vectorstore.similarity_search_with_score(
            query,
            filter={"doc_id": {"$in": [doc1_id, doc2_id]}},
            k=5
        )

        # Separate chunks by document
        doc1_chunks = [chunk for chunk, _ in search_results if chunk.metadata["doc_id"] == doc1_id]
        doc2_chunks = [chunk for chunk, _ in search_results if chunk.metadata["doc_id"] == doc2_id]

        # Create comparison prompt
        comparison_prompt = PromptTemplate(
            template="""
            Compare the following excerpts from two documents:

            Document 1:
            {doc1_content}

            Document 2:
            {doc2_content}

            Please provide a detailed comparison focusing on:
            1. Key similarities
            2. Major differences
            3. Unique points in each document
            4. Overall relationship between the content

            Comparison:
            """,
            input_variables=["doc1_content", "doc2_content"]
        )

        # Create and run comparison chain
        comparison_chain = LLMChain(
            llm=self.llm,
            prompt=comparison_prompt
        )

        comparison_result = comparison_chain.run(
            doc1_content="\n".join(chunk.page_content for chunk in doc1_chunks),
            doc2_content="\n".join(chunk.page_content for chunk in doc2_chunks)
        )

        return {
            "comparison": comparison_result,
            "doc1_chunks": [chunk.page_content for chunk in doc1_chunks],
            "doc2_chunks": [chunk.page_content for chunk in doc2_chunks]
        }

    def process_document(self, file, file_type):
        """Process a document from file upload to storage."""
        # Generate document ID
        doc_id = hashlib.md5(file.read()).hexdigest()
        file.seek(0)  # Reset file pointer
        
        # Extract and process text
        text = self.extract_text(file, file_type)
        processed_text = self.preprocess_text(text)
        chunks = self.get_document_chunks(processed_text)
        
        # Store chunks
        self.store_document(chunks, doc_id)
        
        return doc_id