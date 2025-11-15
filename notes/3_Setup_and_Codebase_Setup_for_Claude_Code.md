# 3. Setup and Codebase Setup for Claude Code

## Getting Started with Claude Code

### Accessing Claude Code

To launch Claude Code in your terminal:

```bash
claude
```

This opens an interactive session where you can chat with your codebase.

---

## Understanding Your Codebase

### Using Claude Code as an Explainer

Claude Code excels at helping you understand existing codebases. Rather than manually searching through files, you can ask high-level questions and Claude will agentically search for relevant information.

### Key Approach

> **Best Practice**: Use Claude Code as an explainer first before asking it to write code. This helps you better understand what's happening in your application.

### Example Questions

**High-level overview:**

```text
What does this codebase do?
```

**Specific processes:**

```text
How are these documents processed?
```

**Request visualizations:**

```text
Draw a diagram that illustrates this flow
```

---

## The CLAUDE.md File System

### Overview

CLAUDE.md files provide persistent memory and instructions for Claude Code across sessions.

### Three Types of CLAUDE.md Files

| File Type | Location | Purpose | Sharing |
|-----------|----------|---------|---------|
| **Project** | Project root | Project-specific instructions | Committed to git, shared with team |
| **Local** | Project root | Personal preferences for this project | Git-ignored, private |
| **Global** | `~/.claude/` | Instructions for all projects | User-specific, affects all projects |

### Initializing CLAUDE.md

Use the `/init` command to automatically generate a CLAUDE.md file:

```bash
/init
```

This command:

- Analyzes your codebase structure
- Identifies key technologies
- Creates architectural documentation
- Generates component descriptions

### Example CLAUDE.md Structure

**Real example from demo2/chatbot-rag project:**

```markdown
# Project Overview
This is a RAG (Retrieval Augmented Generation) chatbot application with 
document processing capabilities. The system allows users to upload documents 
(PDF, DOCX, XLSX, PPTX, TXT, MD), stores them in a vector database, and uses 
semantic search to provide context-aware responses via Google Gemini AI.

# Key Technologies
- FastAPI (Backend API)
- Gradio (Frontend UI)
- ChromaDB (Vector Database)
- Google Gemini AI (LLM)
- Sentence Transformers (Embeddings)
- Three.js & D3.js (Visualizations)

# Architectural Overview
Two-server architecture:
1. Backend (FastAPI) - Port 8000
   - REST API endpoints
   - Document processing and chunking
   - RAG engine with ChromaDB vector store
   - Gemini API integration
   - Session management

2. Frontend (Gradio) - Port 7860
   - Web UI with chat interface
   - File upload handling
   - HTTP client to backend API
   - Three.js/D3.js visualizations

# Core Components
- DocumentProcessor: Extracts and chunks text from multiple file formats
- RAGEngine: Handles semantic search and response generation
- FastAPI Backend: API endpoints and request handling
- Gradio Frontend: User interface and interactions

# Development Guidelines
- Always use uv to run the servers, do not use pip directly
- Both backend and frontend must be running simultaneously
- Backend must start before frontend (20 second wait recommended)
- Check logs/backend.log for debugging
```

### Adding to Memory

Quick command to add instructions:

```bash
# Always use UV to run the server, do not use pip directly
```

This adds the instruction to your selected CLAUDE.md file (Project, Local, or User).

**Real example from demo2:**

The chatbot-rag project includes this instruction in CLAUDE.md:

```markdown
## Dependencies Management

Uses **uv** (modern Python package manager):
- `uv sync`: Install/update all dependencies
- `uv run <command>`: Run command in virtual environment
- `.venv/` directory auto-created (do not commit)
- `pyproject.toml`: Single source of truth for dependencies

No requirements.txt or setup.py files exist.
- Always use uv to run the srvers and do not run pip
```

---

## Essential Claude Code Commands

### Navigation and Help

| Command | Description | Use Case |
|---------|-------------|----------|
| `/help` | Show all available commands | Getting started, reference |
| `/init` | Initialize CLAUDE.md file | First-time setup |
| `/ide` | Connect to VS Code | Enable file context tracking |
| `/clear` | Clear conversation history | Starting fresh on new features |
| `/compact` | Clear history but keep summary | Reducing context while maintaining continuity |
| `Esc` | Interrupt current process | Stopping unwanted operations |

### Memory Management

```bash
# Add to project memory (shared with team)
# [instruction] → Select "Project memory"

# Add to local memory (personal only)
# [instruction] → Select "Local memory"

# Add to global memory (all projects)
# [instruction] → Select "User memory"
```

---

## IDE Integration

### Connecting to Visual Studio Code

```bash
/ide
```

**Benefits:**

- Real-time file context tracking
- Visual diff viewing for changes
- Automatic file tagging when browsing
- Permission prompts for file modifications

### Human-in-the-Loop Safety

Claude Code asks for permission before:

- Creating new files
- Modifying existing files
- Executing commands

**Options:**

1. Approve each change individually
2. Auto-accept all edits (use with caution)

---

## Working with Git

### Automated Git Operations

Claude Code can handle git operations with intelligent commit messages.

**Example workflow:**

```bash
# Claude Code will:
# 1. Stage the appropriate files
# 2. Generate descriptive commit messages
# 3. Commit the changes

# User request:
Add and commit these changes
```

**Benefits:**

- Descriptive commit messages automatically generated
- Consistent commit message format
- Better git history for team collaboration
- Easier to track historical changes

---

## Best Practices

### 1. Start with Understanding

Before writing code, use Claude Code to:

- Get an overview of the codebase
- Understand the architecture
- Identify key components
- Learn the development workflow

### 2. Leverage Visualization

Request diagrams and visualizations to understand:

- Data flow
- System architecture
- Process sequences
- Component relationships

### 3. Use CLAUDE.md Effectively

**Project-level instructions (from demo2/chatbot-rag):**

```markdown
## Development Commands

### Starting the Application
**Option 1 - Automated (Recommended)**:
./start.sh

**Option 2 - Manual (Two Terminals)**:
# Terminal 1 - Backend
cd backend
uv run python main.py

# Terminal 2 - Frontend
cd frontend
uv run python app.py

## Critical Gotchas

### State Persistence
- ChromaDB: May be in-memory depending on config
- Session History: Definitely in-memory, lost on restart
- Uploaded Files: Persisted to uploads/ directory

### Dependencies
- Pydantic >=2.7.4: Required by LangChain
- Aiofiles <25.0: Gradio compatibility constraint
- SentenceTransformer model: First run downloads ~80MB

### Security Considerations
- CORS: allow_origins=["*"] (development only)
- No authentication on any endpoints
- No file size limits enforced
- No rate limiting
```

**Personal preferences (local):**

```markdown
- Use 2-space indentation
- Prefer async/await syntax
- Include type hints
- Log all errors to logs/backend.log
```

### 4. Manage Context Window

- Use `/clear` when switching to unrelated tasks
- Use `/compact` to maintain summary while reducing tokens
- Press `Esc` to interrupt unnecessary operations

### 5. Utilize Commands

Familiarize yourself with built-in commands:

- Custom commands can be created (covered in advanced lessons)
- Use `/help` as a quick reference
- Commands save time and ensure consistency

---

## Example: Running the Application

### Real Example from demo2/chatbot-rag

**Setup Steps:**

1. **Configure Environment Variables**

   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

2. **Install Dependencies** (using UV)

   ```bash
   uv sync
   ```

   This creates `.venv/` automatically and installs all dependencies from `pyproject.toml`.

3. **Start the Application**

   **Option 1 - Automated (Recommended):**

   ```bash
   ./start.sh
   ```

   This script:
   - Checks for .env file
   - Installs dependencies with `uv sync`
   - Creates upload/data/logs directories
   - Starts backend in background
   - Waits 20 seconds for backend initialization
   - Starts frontend in foreground

   **Option 2 - Manual (Two Terminals):**

   ```bash
   # Terminal 1 - Backend
   cd backend
   uv run python main.py

   # Terminal 2 - Frontend
   cd frontend
   uv run python app.py
   ```

4. **Access the Application**
   - Backend: <http://localhost:8000>
   - Frontend: <http://localhost:7860>

**Testing the API:**

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

---

## Key Takeaways

1. **Claude Code as an Explainer**: Use it to understand codebases before writing code
2. **CLAUDE.md is Critical**: Provides persistent memory and project-specific instructions
3. **Agentic Search**: Claude intelligently finds relevant files rather than requiring manual navigation
4. **IDE Integration**: VS Code integration provides visual feedback and safety controls
5. **Git Automation**: Automated, descriptive commits improve team collaboration
6. **Context Management**: Use commands like `/clear` and `/compact` to optimize the context window
7. **Permission-Based**: Human-in-the-loop prevents unintended changes

---

### File Structure Example

**Generic structure:**

```text
project/
├── CLAUDE.md              # Project-wide instructions (git tracked)
├── CLAUDE.local.md        # Personal preferences (git-ignored)
├── frontend/
│   └── CLAUDE.md          # Frontend-specific instructions
├── backend/
│   └── CLAUDE.md          # Backend-specific instructions
└── ~/.claude/
    └── CLAUDE.md          # Global instructions (all projects)
```

**Real example from demo2/chatbot-rag:**

```text
chatbot-rag/
├── CLAUDE.md              # Comprehensive project documentation
├── ARCHITECTURE.md        # System architecture details
├── README.md              # User-facing documentation
├── QUICKSTART.md          # Quick setup guide
├── pyproject.toml         # Dependencies (uv format)
├── .env.example           # Environment variable template
├── .gitignore             # Git ignore rules
├── start.sh               # Automated startup script
├── backend/
│   ├── main.py            # FastAPI application
│   ├── rag_engine.py      # RAG implementation
│   └── document_processor.py  # Document processing
├── frontend/
│   └── app.py             # Gradio interface
├── static/
│   ├── css/
│   │   └── custom.css     # Styling
│   └── js/
│       ├── threejs-background.js  # 3D animations
│       └── d3-visualization.js    # Analytics charts
├── uploads/               # Uploaded documents
├── data/                  # ChromaDB storage
└── logs/                  # Application logs
```

---

## Real-World Example: Building demo2/chatbot-rag

### How Claude Code Was Used

The demo2/chatbot-rag project demonstrates practical Claude Code usage:

#### 1. Initial Setup with `/init`

```bash
/init
```

This generated the comprehensive CLAUDE.md file with:

- Project overview and architecture
- Technology stack documentation
- Development commands and workflows
- Critical gotchas and configuration details

#### 2. Understanding the Codebase

**Example questions asked:**

```text
What does this codebase do?
```

Claude Code analyzed the project and explained:

- Two-server architecture (FastAPI + Gradio)
- RAG implementation with ChromaDB
- Document processing pipeline
- API endpoints and data flow

```text
How are documents processed?
```

Claude Code traced through:

- DocumentProcessor class methods
- Text extraction for different file types
- Chunking algorithm with smart boundaries
- Embedding generation and storage

#### 3. Adding Project-Specific Instructions

```bash
# Always use uv to run the servers, do not use pip directly
```

This was added to CLAUDE.md to ensure consistent dependency management.

#### 4. Generating Documentation

Claude Code helped create:

- **ARCHITECTURE.md**: Detailed system architecture with diagrams
- **QUICKSTART.md**: Quick setup guide for new users
- **README.md**: Comprehensive user-facing documentation
- **MIGRATION_NOTES.md**: Notes on dependency updates

#### 5. Troubleshooting and Debugging

**Example request:**

```text
The backend won't start. Check the logs and help me debug.
```

Claude Code:

- Read `logs/backend.log`
- Identified missing GEMINI_API_KEY
- Suggested checking `.env` file
- Provided setup commands

#### 6. Code Modifications

**Example request:**

```text
Add support for XLSX files in the document processor
```

Claude Code:

1. Located `document_processor.py`
2. Added `openpyxl` to dependencies in `pyproject.toml`
3. Implemented `_extract_from_xlsx()` method
4. Updated file extension routing
5. Updated frontend file type filter

#### 7. Creating Startup Scripts

**Example request:**

```text
Create a startup script that runs both servers automatically
```

Claude Code created `start.sh` with:

- Environment validation
- Dependency installation
- Directory creation
- Background backend process
- Timed frontend startup
- Error handling

### Key Insights from demo2

1. **CLAUDE.md is Essential**: The 289-line CLAUDE.md file contains critical information about:
   - Two-server architecture requirements
   - Hardcoded values that need code changes
   - State persistence behavior
   - Security considerations
   - Performance characteristics

2. **Documentation Hierarchy**: Multiple documentation files serve different purposes:
   - CLAUDE.md: For Claude Code (technical details)
   - README.md: For users (setup and usage)
   - ARCHITECTURE.md: For developers (system design)
   - QUICKSTART.md: For quick starts (minimal steps)

3. **Project-Specific Commands**: The CLAUDE.md includes exact commands:
   - `uv sync` for dependencies
   - `uv run python main.py` for execution
   - `./start.sh` for automated startup
   - API testing with curl commands

4. **Critical Gotchas Documented**: Important details captured:
   - Backend must start before frontend (20s wait)
   - Session history is in-memory (lost on restart)
   - First run downloads 80MB embedding model
   - CORS allows all origins (development only)

5. **Technology Stack Clarity**: Clear documentation of:
   - FastAPI 0.109.0 for backend
   - Gradio 4.16.0 for frontend
   - ChromaDB 0.4.22 for vector storage
   - Gemini Pro for LLM
   - all-MiniLM-L6-v2 for embeddings

---

## Glossary

**RAG (Retrieval Augmented Generation)**: A technique that enhances LLM responses by retrieving relevant context from a knowledge base before generating answers.

**Vector Database**: A specialized database for storing and querying high-dimensional vectors, enabling efficient similarity search.

**Agentic Search**: Autonomous searching where the AI decides which files and components to examine based on the query.

**Context Window**: The amount of text (measured in tokens) that an LLM can process in a single conversation.

**ChromaDB**: An open-source vector database used for storing and querying embeddings.
