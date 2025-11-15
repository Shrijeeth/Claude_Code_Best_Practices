from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import shutil
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv
import uuid

from document_processor import DocumentProcessor
from rag_engine import RAGEngine

load_dotenv()

app = FastAPI(title="Chatbot RAG API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize directories
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize RAG engine
rag_engine = RAGEngine()
document_processor = DocumentProcessor()


class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    use_rag: bool = True


class ChatResponse(BaseModel):
    response: str
    session_id: str
    sources: Optional[List[str]] = None


@app.get("/")
async def root():
    return {"message": "Chatbot RAG API is running"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload and process a document for RAG"""
    try:
        # Save uploaded file
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process document
        text_chunks = document_processor.process_document(str(file_path))

        if not text_chunks:
            raise HTTPException(status_code=400, detail="Could not extract text from document")

        # Add to vector store
        doc_id = rag_engine.add_documents(text_chunks, file.filename)

        return {
            "status": "success",
            "filename": file.filename,
            "chunks_processed": len(text_chunks),
            "document_id": doc_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@app.post("/chat", response_model=ChatResponse)
async def chat(chat_message: ChatMessage):
    """Chat endpoint with optional RAG"""
    try:
        session_id = chat_message.session_id or str(uuid.uuid4())

        if chat_message.use_rag:
            # Use RAG to get relevant context
            response, sources = rag_engine.generate_response(
                chat_message.message,
                session_id
            )
            return ChatResponse(
                response=response,
                session_id=session_id,
                sources=sources
            )
        else:
            # Direct chat without RAG
            model = genai.GenerativeModel(os.getenv("GEMINI_MODEL"))
            response = model.generate_content(chat_message.message)
            return ChatResponse(
                response=response.text,
                session_id=session_id
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")


@app.delete("/documents")
async def clear_documents():
    """Clear all documents from vector store"""
    try:
        rag_engine.clear_all()
        return {"status": "success", "message": "All documents cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing documents: {str(e)}")


@app.get("/documents")
async def list_documents():
    """List all uploaded documents"""
    try:
        documents = rag_engine.list_documents()
        return {"documents": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
