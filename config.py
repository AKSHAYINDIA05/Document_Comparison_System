import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_ENDPOINT_EMBEDDINGS = os.getenv("AZURE_OPENAI_ENDPOINT_EMBEDDINGS")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")
AZURE_EMBEDDINGS_DEPLOYMENT_NAME = os.getenv("AZURE_EMBEDDINGS_DEPLOYMENT_NAME")
AZURE_API_VERSION = "2024-02-15-preview"

# ChromaDB Configuration
CHROMA_PERSIST_DIRECTORY = "./chroma_db"

# Document Processing Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Supported File Types
SUPPORTED_FILES = [
    "txt", "pdf", "docx"
]

# FastAPI Configuration
BACKEND_PORT = 8000
BACKEND_HOST = "localhost"
BACKEND_URL = "https://document-comparison-system.onrender.com/"