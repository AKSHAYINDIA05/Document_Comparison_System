# Document Comparison System using RAG

A Retrieval Augmented Generation (RAG) based system for performing contextual comparisons between two documents. This system uses Azure OpenAI for language processing and embeddings, ChromaDB for vector storage, FastAPI for the backend, and Streamlit for the user interface.

## Features

- Upload and process multiple document formats (PDF, DOCX, TXT)
- RAG-based document comparison with semantic search
- Interactive web interface with side-by-side comparison view
- Custom comparison queries
- Downloadable comparison results
- Efficient document chunking and processing
- Vector storage with ChromaDB
- REST API backend with FastAPI

## Prerequisites

- Python 3.8+
- Azure OpenAI API access
- Sufficient storage space for the vector database

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd document-comparison-system
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your Azure OpenAI credentials:
```
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_DEPLOYMENT_NAME=your_deployment_name
AZURE_EMBEDDINGS_DEPLOYMENT_NAME=your_embeddings_deployment_name
```

## Project Structure

```
project_root/
├── app.py           # Streamlit frontend
├── backend.py       # FastAPI backend
├── processor.py     # Document processing and RAG logic
├── config.py        # Configuration settings
└── requirements.txt # Project dependencies
```

## Running the Application

1. Start the backend server:
```bash
python backend.py
```

2. In a new terminal, start the Streamlit frontend:
```bash
streamlit run app.py
```

3. Open your browser and navigate to `http://localhost:8501` to access the application.

## Usage

1. Upload Documents:
   - Use the file upload widgets to upload two documents for comparison
   - Supported formats: PDF, DOCX, TXT
   - Wait for the processing confirmation

2. Compare Documents:
   - Once both documents are uploaded, you can start the comparison
   - Optionally enter a custom comparison query
   - Click "Compare Documents" to generate the analysis

3. View Results:
   - The comparison results are displayed in three tabs:
     - Comparison: Overall analysis
     - Document 1 Excerpts: Relevant segments from the first document
     - Document 2 Excerpts: Relevant segments from the second document
   - Download the complete results as a JSON file

4. Reset:
   - Use the "Reset" button to clear the current session and start over

## API Endpoints

The FastAPI backend provides the following endpoints:

### POST /upload
Upload and process a single document.
- Request: Multipart form data with file
- Response: Document ID and success message

### POST /compare
Compare two documents.
- Parameters:
  - doc1_id: ID of first document
  - doc2_id: ID of second document
  - query: Optional custom comparison query
- Response: Comparison results including analysis and relevant excerpts

## Configuration

Key configuration settings in `config.py`:

- `CHUNK_SIZE`: Size of document chunks (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200)
- `SUPPORTED_FILES`: List of supported file types
- `CHROMA_PERSIST_DIRECTORY`: Location for vector database storage

## Technical Details

### Document Processing
- Documents are split into chunks using RecursiveCharacterTextSplitter
- Text is preprocessed to remove special characters and normalize whitespace
- Each chunk is embedded using Azure OpenAI embeddings
- Chunks are stored in ChromaDB with document metadata

### RAG Implementation
- Uses similarity search to find relevant chunks from both documents
- Implements hybrid search through ChromaDB's search capabilities
- Custom prompts for generating comparative analysis
- Configurable retrieval parameters

### Vector Storage
- ChromaDB is used for efficient vector storage and retrieval
- Persistent storage enables caching of processed documents
- Metadata filtering for document-specific searches

## Error Handling

The system includes comprehensive error handling for:
- Unsupported file types
- Processing failures
- API communication errors
- Invalid document IDs

## Future Improvements

Potential enhancements:
- Support for more file formats
- Advanced reranking algorithms
- Multimodal document comparison
- User authentication
- Comparison history
- More sophisticated chunking strategies
- Advanced caching mechanisms

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.