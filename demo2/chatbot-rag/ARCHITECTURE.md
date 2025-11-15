# 🏗️ Architecture Documentation

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         USER BROWSER                         │
│                     http://localhost:7860                    │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    GRADIO FRONTEND                           │
│  ┌─────────────┬──────────────┬──────────────────────────┐  │
│  │  Chat UI    │  File Upload │  Document Management     │  │
│  │  (Gradio)   │  Interface   │  Controls                │  │
│  └─────────────┴──────────────┴──────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Visualization Layer                                 │   │
│  │  - Three.js: 3D Particle System & Wave Animation    │   │
│  │  - D3.js: Real-time Chat Analytics Charts           │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/REST API
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND                           │
│                   http://localhost:8000                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  API Endpoints                                       │   │
│  │  - POST /upload    : Upload & process documents      │   │
│  │  - POST /chat      : Chat with RAG                   │   │
│  │  - GET /documents  : List documents                  │   │
│  │  - DELETE /documents : Clear all documents           │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Document Processor                                  │   │
│  │  - PDF, DOCX, TXT, MD, XLSX, PPTX support           │   │
│  │  - Text chunking with overlap                        │   │
│  │  - Smart sentence boundary detection                 │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  RAG Engine                                          │   │
│  │  - Document indexing                                 │   │
│  │  - Semantic search                                   │   │
│  │  - Context retrieval                                 │   │
│  │  - Response generation                               │   │
│  └──────────────────────────────────────────────────────┘   │
└───────┬─────────────────────────┬────────────────────────────┘
        │                         │
        ▼                         ▼
┌──────────────────┐    ┌────────────────────────┐
│  VECTOR DATABASE │    │   GEMINI AI API        │
│   (ChromaDB)     │    │  (Google)              │
│                  │    │                        │
│  - Embeddings    │    │  - gemini-pro model    │
│  - Similarity    │    │  - Text generation     │
│    Search        │    │  - Context understanding│
└──────────────────┘    └────────────────────────┘
```

## Component Details

### Frontend Layer

#### Gradio Interface (`frontend/app.py`)
- **Purpose**: User interface and interaction
- **Features**:
  - Chat interface with message history
  - File upload with drag-and-drop
  - Document management controls
  - Real-time status updates
  - Session management

#### Three.js Animation (`static/js/threejs-background.js`)
- **Purpose**: Immersive 3D background
- **Features**:
  - 1500 animated particles with color gradients
  - Wave mesh with real-time deformation
  - Mouse interaction and tracking
  - Point lights with multiple colors
  - Responsive to window resize

#### D3.js Visualization (`static/js/d3-visualization.js`)
- **Purpose**: Data visualization and analytics
- **Features**:
  - Real-time message activity chart
  - Animated statistics cards
  - Time-series data aggregation
  - Smooth transitions and updates
  - Gradient fills and styling

#### Custom Styling (`static/css/custom.css`)
- **Purpose**: Modern UI/UX
- **Features**:
  - Glassmorphism design
  - Dark theme with gradients
  - Smooth animations
  - Responsive layout
  - Custom scrollbars

### Backend Layer

#### FastAPI Server (`backend/main.py`)
- **Purpose**: API server and request handling
- **Endpoints**:
  - `GET /`: Health check
  - `POST /upload`: Document upload and processing
  - `POST /chat`: Chat with RAG support
  - `GET /documents`: List all documents
  - `DELETE /documents`: Clear vector store
- **Features**:
  - CORS middleware
  - Async request handling
  - Error handling
  - File management

#### Document Processor (`backend/document_processor.py`)
- **Purpose**: Extract and chunk document text
- **Supported Formats**:
  - PDF (via pypdf)
  - DOCX (via python-docx)
  - XLSX (via openpyxl)
  - PPTX (via python-pptx)
  - TXT, MD (plain text)
- **Processing**:
  - Text extraction
  - Chunk size: 1000 characters
  - Overlap: 200 characters
  - Smart sentence boundary detection

#### RAG Engine (`backend/rag_engine.py`)
- **Purpose**: Retrieval Augmented Generation
- **Components**:
  - **Vector Store**: ChromaDB with cosine similarity
  - **Embeddings**: all-MiniLM-L6-v2 (384 dimensions)
  - **LLM**: Gemini Pro
- **Features**:
  - Document indexing
  - Semantic similarity search
  - Context-aware response generation
  - Session history management
  - Source attribution

## Data Flow

### Document Upload Flow

```
User uploads file
     │
     ▼
Frontend sends to /upload
     │
     ▼
Backend saves file
     │
     ▼
Document Processor extracts text
     │
     ▼
Text split into chunks
     │
     ▼
Embeddings generated (SentenceTransformer)
     │
     ▼
Chunks + embeddings stored in ChromaDB
     │
     ▼
Success response to frontend
```

### Chat Flow (with RAG)

```
User sends message
     │
     ▼
Frontend sends to /chat
     │
     ▼
RAG Engine generates query embedding
     │
     ▼
ChromaDB finds top-k similar chunks (k=5)
     │
     ▼
Context built from retrieved chunks
     │
     ▼
Prompt constructed with context + history
     │
     ▼
Gemini API generates response
     │
     ▼
Response + sources sent to frontend
     │
     ▼
Display in chat UI
```

## Technology Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| FastAPI | 0.109.0 | Web framework |
| Uvicorn | 0.27.0 | ASGI server |
| Google Generative AI | 0.3.2 | Gemini API client |
| ChromaDB | 0.4.22 | Vector database |
| Sentence Transformers | 2.3.1 | Text embeddings |
| LangChain | 0.1.4 | RAG framework |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| Gradio | 4.16.0 | UI framework |
| Three.js | r128 | 3D graphics |
| D3.js | v7 | Data visualization |

### Document Processing
| Library | Purpose |
|---------|---------|
| pypdf | PDF processing |
| python-docx | Word documents |
| openpyxl | Excel files |
| python-pptx | PowerPoint files |

## Performance Considerations

### Embedding Model
- **Model**: all-MiniLM-L6-v2
- **Dimensions**: 384
- **Speed**: ~700 sentences/sec on CPU
- **Quality**: Good balance for most use cases

### Vector Search
- **Algorithm**: HNSW (Hierarchical Navigable Small World)
- **Distance Metric**: Cosine similarity
- **Search Time**: O(log n) approximate
- **Top-k**: 5 results (configurable)

### Chunking Strategy
- **Chunk Size**: 1000 characters
  - Large enough for context
  - Small enough for precision
- **Overlap**: 200 characters
  - Prevents context loss at boundaries
- **Sentence-aware**: Breaks at sentence boundaries

## Security Considerations

### API Keys
- Stored in `.env` file (not in version control)
- Loaded via python-dotenv
- Never exposed to frontend

### File Uploads
- Validated file extensions
- Stored in isolated directory
- Size limits enforced by web server

### CORS
- Currently allows all origins (development)
- Should be restricted in production

## Scalability

### Current Limitations
- In-memory ChromaDB (resets on restart)
- Single-threaded embedding generation
- File storage on local disk

### Production Improvements
- Persistent ChromaDB with disk storage
- Batch embedding generation
- Cloud storage for files (S3, GCS)
- Redis for session management
- Load balancer for multiple workers
- GPU acceleration for embeddings

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | Yes | - | Google Gemini API key |
| `API_URL` | No | http://localhost:8000 | Backend API URL |
| `GEMINI_MODEL` | No | gemini-pro | Gemini model to use |
| `CHROMA_PERSIST_DIRECTORY` | No | ./data/chroma | ChromaDB storage |

## Monitoring and Debugging

### Logs
- Backend: Console output with request/response info
- Frontend: Browser console for JavaScript errors
- ChromaDB: Internal logging for vector operations

### Analytics
- Message count tracking
- File upload tracking
- RAG query tracking
- Time-series message activity

## Future Enhancements

1. **Multi-user Support**
   - User authentication
   - Per-user document collections
   - Shared documents

2. **Advanced RAG**
   - Hybrid search (keyword + semantic)
   - Re-ranking of results
   - Query expansion
   - Citation generation

3. **UI Improvements**
   - Voice input/output
   - Code syntax highlighting
   - Markdown rendering
   - Export conversations

4. **Performance**
   - Caching frequently asked questions
   - Streaming responses
   - Background document processing
   - GPU acceleration

5. **Additional Features**
   - Multi-language support
   - Image/video upload
   - Table extraction from PDFs
   - Collaborative editing
