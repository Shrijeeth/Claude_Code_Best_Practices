import os
import shutil
import uuid
from pathlib import Path

import google.generativeai as genai
from document_processor import DocumentProcessor
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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
    session_id: str | None = None
    use_rag: bool = True


class ChatResponse(BaseModel):
    response: str
    session_id: str
    sources: list[str] | None = None


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
            "document_id": doc_id,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {e!s}") from e


@app.post("/chat", response_model=ChatResponse)
async def chat(chat_message: ChatMessage):
    """Chat endpoint with optional RAG"""
    try:
        session_id = chat_message.session_id or str(uuid.uuid4())

        if chat_message.use_rag:
            # Use RAG to get relevant context
            response, sources = rag_engine.generate_response(chat_message.message, session_id)
            return ChatResponse(response=response, session_id=session_id, sources=sources)
        else:
            # Direct chat without RAG
            model = genai.GenerativeModel(os.getenv("GEMINI_MODEL"))
            response = model.generate_content(chat_message.message)
            return ChatResponse(response=response.text, session_id=session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {e!s}") from e


@app.delete("/documents")
async def clear_documents():
    """Clear all documents from vector store"""
    try:
        rag_engine.clear_all()
        return {"status": "success", "message": "All documents cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing documents: {e!s}") from e


@app.get("/documents")
async def list_documents():
    """List all uploaded documents"""
    try:
        documents = rag_engine.list_documents()
        return {"documents": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing documents: {e!s}") from e


@app.get("/sessions")
async def list_sessions():
    """List all chat sessions"""
    try:
        sessions = rag_engine.session_manager.list_sessions()
        return {"sessions": sessions, "total": len(sessions)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing sessions: {e!s}") from e


@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Get details of a specific session"""
    try:
        session_data = rag_engine.session_manager.export_session(session_id)
        if session_data is None:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        return session_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving session: {e!s}") from e


@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a specific session"""
    try:
        deleted = rag_engine.session_manager.delete_session(session_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        return {"status": "success", "message": f"Session {session_id} deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting session: {e!s}") from e


@app.delete("/sessions")
async def clear_all_sessions():
    """Clear all chat sessions"""
    try:
        rag_engine.session_manager.clear_all_sessions()
        return {"status": "success", "message": "All sessions cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing sessions: {e!s}") from e


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
