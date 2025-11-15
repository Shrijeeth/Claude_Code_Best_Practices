# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a RAG (Retrieval Augmented Generation) chatbot application with document processing capabilities. The system allows users to upload documents (PDF, DOCX, XLSX, PPTX, TXT, MD), stores them in a vector database, and uses semantic search to provide context-aware responses via Google Gemini AI.

## Architecture

### Two-Server Architecture

The application runs as **two independent servers** that must both be running:

1. **Backend** (FastAPI) - Port 8000
   - REST API endpoints
   - Document processing and chunking
   - RAG engine with ChromaDB vector store
   - Gemini API integration
   - Session management

2. **Frontend** (Gradio) - Port 7860
   - Web UI with chat interface
   - File upload handling
   - HTTP client to backend API
   - Three.js/D3.js visualizations

**Critical**: Frontend does NOT maintain conversation state. All session history lives in the backend's `rag_engine.session_history` in-memory dictionary, keyed by session_id.

### Component Interactions

```
User Browser (port 7860)
    ↓ HTTP
Gradio Frontend (frontend/app.py)
    ↓ REST API (requests.post)
FastAPI Backend (backend/main.py)
    ↓
RAG Engine (backend/rag_engine.py)
    ↓
ChromaDB Vector Store + SentenceTransformer + Gemini API
```

### Data Flow Patterns

**Document Upload**:
1. Frontend → POST /upload with multipart file
2. Backend saves to `uploads/` directory
3. DocumentProcessor extracts text based on file extension
4. Text chunked with smart sentence-boundary detection (1000 chars, 200 overlap)
5. SentenceTransformer generates 384-dim embeddings
6. ChromaDB stores embeddings + text + metadata (source, doc_id, chunk_index, timestamp)

**Chat with RAG**:
1. Frontend → POST /chat with `{message, session_id, use_rag}`
2. Query encoded to 384-dim vector
3. ChromaDB cosine similarity search returns top-5 chunks
4. Prompt constructed: context (5 chunks) + session history (last 6 messages) + user question
5. Gemini API generates response
6. Session history updated (rolling 10-message window)
7. Response + sources + session_id returned to frontend

**Chat without RAG**:
1. Frontend → POST /chat with `use_rag=false`
2. Direct Gemini API call (no retrieval)
3. General knowledge response only

## Development Commands

### Starting the Application

**Option 1 - Automated (Recommended)**:
```bash
./start.sh
```
This script:
- Checks for .env file
- Installs dependencies with `uv sync`
- Creates upload/data/logs directories
- Starts backend in background (PID tracked for cleanup)
- Waits 20 seconds for backend initialization
- Starts frontend in foreground

**Option 2 - Manual (Two Terminals)**:
```bash
# Terminal 1 - Backend
cd backend
uv run python main.py

# Terminal 2 - Frontend
cd frontend
uv run python app.py
```

### Environment Setup

```bash
# First time setup
cp .env.example .env
# Edit .env and set GEMINI_API_KEY

# Install dependencies (creates .venv automatically)
uv sync
```

### Testing the Application

No automated test suite exists. Manual testing:

1. Upload a document via UI (right panel)
2. Ask a question with RAG enabled
3. Verify sources are cited in response
4. Check `logs/backend.log` for errors

### API Testing

```bash
# Health check
curl http://localhost:8000/

# Upload document
curl -X POST "http://localhost:8000/upload" \
  -F "file=@test.pdf"

# Chat with RAG
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is this about?", "use_rag": true}'

# List documents
curl http://localhost:8000/documents

# Clear all documents
curl -X DELETE http://localhost:8000/documents
```

## Code Architecture Details

### DocumentProcessor (backend/document_processor.py)

**Design Pattern**: Plugin-style processor with format-specific extractors

- Each file type has its own `_extract_from_*()` method
- Main `process_document()` routes based on file extension
- Returns list of text chunks ready for embedding

**Chunking Algorithm**:
- Target: 1000 characters per chunk
- Overlap: 200 characters (provides context continuity)
- Smart boundary detection: Tries to break at sentence endings (`. `, `? `, `! `)
- Only breaks at sentence if it's at least 50% through chunk (prevents tiny chunks)

**Adding New File Types**: Add new `_extract_from_*()` method and update extension mapping in `process_document()`.

### RAGEngine (backend/rag_engine.py)

**Critical Implementation Details**:

1. **Embedding Model**: `all-MiniLM-L6-v2` produces 384-dimensional vectors
   - Changing this model requires rebuilding the entire vector store
   - No version pinning in code (could break on model updates)

2. **Session History**: In-memory dictionary `{session_id: [messages]}`
   - Stores last 10 messages per session
   - Includes last 6 messages in prompts (3 exchanges)
   - Lost on application restart
   - No persistence mechanism

3. **ChromaDB Configuration**:
   - Distance metric: Cosine similarity (`hnsw:space: cosine`)
   - Collection name: "documents"
   - No authentication or multi-tenancy
   - In-memory by default (check CHROMA_PERSIST_DIRECTORY env var)

4. **Retrieval**: Always fetches top-5 chunks (hardcoded `n_results=5`)

5. **Prompt Engineering**: Template in `generate_response()` lines 96-115
   - Instructs model to prefer document context
   - Falls back to general knowledge if no context
   - Maintains conversational continuity via history

### Frontend Architecture (frontend/app.py)

**State Management**:
- Global `session_id` variable tracks conversation
- Updated from backend responses
- None on first message → backend generates UUID

**Event Handlers**:
- `chat()`: Main message handler (lines 33-78)
- `upload_file()`: Document upload (lines 15-30)
- `list_documents()`: Query backend for docs (lines 92-108)
- `clear_documents()`: Delete all from vector store (lines 80-89)

**UI Updates**: Gradio automatically re-renders when output values change

**Visualization Integration**:
- `static/js/threejs-background.js`: Particle system (1500 particles, wave mesh)
- `static/js/d3-visualization.js`: Real-time analytics (message counts, activity chart)
- Both injected via custom HTML/JS in Gradio

## Configuration

### Hardcoded Values (Require Code Changes)

- Chunk size: 1000 characters (`DocumentProcessor.__init__`)
- Chunk overlap: 200 characters (`DocumentProcessor.__init__`)
- Retrieval count: 5 chunks (`RAGEngine.retrieve_relevant_chunks`)
- Session history limit: 10 messages (`RAGEngine.generate_response` line 123)
- Prompt history included: 6 messages (`RAGEngine._format_history` line 136)
- Backend startup wait: 20 seconds (`start.sh` line 38)

### Environment Variables (.env)

Required:
- `GEMINI_API_KEY`: Google Gemini API key

Optional:
- `API_URL`: Backend URL (default: http://localhost:8000)
- `GEMINI_MODEL`: Model name (default: gemini-pro)
- `CHROMA_PERSIST_DIRECTORY`: ChromaDB storage path (default: ./data/chroma)

## Critical Gotchas

### State Persistence
- **ChromaDB**: May be in-memory depending on ChromaDB version/config. Check if data persists across restarts.
- **Session History**: Definitely in-memory. All conversation context lost on backend restart.
- **Uploaded Files**: Persisted to `uploads/` directory (survives restarts).

### Dependencies
- **Pydantic >=2.7.4**: Required by LangChain (not obvious from direct imports)
- **Aiofiles <25.0**: Gradio compatibility constraint
- **SentenceTransformer model**: First run downloads ~80MB model to cache

### Security Considerations
- CORS: `allow_origins=["*"]` accepts all origins (development setting)
- No authentication on any endpoints
- No file size limits enforced
- No rate limiting
- Uploaded files are never deleted automatically

### Performance
- Embedding generation: ~50ms per query (CPU-bound, no GPU acceleration)
- ChromaDB search: ~20ms for cosine similarity
- Gemini API: 1-3 seconds (network latency, most of total response time)
- Total end-to-end: ~1.2-3.2 seconds

### Error Handling
- Document processing uses generic `HTTPException(500)` for all errors
- Frontend catches all exceptions and shows error messages in chat
- No structured error types or codes
- Backend logs to `logs/backend.log` (check here for debugging)

## Making Changes

### Adding Document Format Support
1. Add extraction library to `pyproject.toml` dependencies
2. Create `_extract_from_<format>()` in `DocumentProcessor`
3. Add file extension to routing logic in `process_document()`
4. Update frontend file_types filter (line 203)

### Modifying RAG Behavior
- **Change chunk size/overlap**: Edit `DocumentProcessor.__init__` parameters
- **Change retrieval count**: Edit `n_results` parameter in `retrieve_relevant_chunks` calls
- **Modify prompt template**: Edit string in `RAGEngine.generate_response` (lines 96-115)
- **Change history window**: Edit line 123 (session storage) and line 136 (prompt inclusion)

### Changing Embedding Model
1. Update model name in `RAGEngine.__init__` line 27
2. Check new model's vector dimensions
3. **Must rebuild entire vector store** (delete `data/` directory)
4. Re-upload all documents

### Switching LLM Provider
1. Replace Gemini imports and configuration
2. Update `RAGEngine.generate_response` lines 118-128
3. Modify prompt format if needed for new provider
4. Update environment variable names

## Dependencies Management

Uses **uv** (modern Python package manager):
- `uv sync`: Install/update all dependencies
- `uv run <command>`: Run command in virtual environment
- `.venv/` directory auto-created (do not commit)
- `pyproject.toml`: Single source of truth for dependencies

No requirements.txt or setup.py files exist.
- Always use uv to run the srvers and do not run pip