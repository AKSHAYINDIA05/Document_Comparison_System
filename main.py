from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import config as config
from processor import DocumentProcessor
import uvicorn

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://document-comparison-system.onrender.com/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize document processor
doc_processor = DocumentProcessor()

@app.post("/upload")
async def upload_document(file: UploadFile):
    """Upload and process a single document."""
    try:
        # Validate file type
        file_extension = file.filename.split('.')[-1].lower()
        if file_extension not in config.SUPPORTED_FILES:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Process document
        doc_id = doc_processor.process_document(file.file, file_extension)
        
        return {"doc_id": doc_id, "message": "Document processed successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compare")
async def compare_documents(doc1_id: str, doc2_id: str, query: str = None):
    """Compare two documents."""
    try:
        comparison_result = doc_processor.compare_documents(doc1_id, doc2_id, query)
        return comparison_result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
