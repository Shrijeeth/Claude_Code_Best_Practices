# 🤖 AI Chatbot with RAG

A modern, interactive chatbot application with Retrieval Augmented Generation (RAG) capabilities, powered by Google's Gemini AI. Features a beautiful UI with Three.js animations and D3.js visualizations.

## ✨ Features

- 💬 **ChatGPT-like Interface**: Clean, modern chat interface built with Gradio
- 📄 **Document Upload**: Support for PDF, DOCX, TXT, MD, XLSX, and PPTX files
- 🧠 **RAG System**: Chat with your documents using advanced retrieval techniques
- 🎨 **Modern UI**: Glassmorphism design with dark theme
- 🌊 **3D Animations**: Interactive Three.js particle system and wave animations
- 📊 **Analytics Dashboard**: Real-time chat analytics with D3.js visualizations
- ⚡ **FastAPI Backend**: High-performance async API
- 🔄 **Session Management**: Maintains conversation context
- 📚 **Vector Database**: ChromaDB for efficient document retrieval

## 🏗️ Architecture

```
chatbot-rag/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── document_processor.py # Document processing utilities
│   └── rag_engine.py        # RAG implementation
├── frontend/
│   └── app.py               # Gradio frontend
├── static/
│   ├── css/
│   │   └── custom.css       # Modern styling
│   └── js/
│       ├── threejs-background.js  # 3D animations
│       └── d3-visualization.js     # Analytics charts
├── uploads/                 # Uploaded documents
├── data/                    # Vector database storage
├── pyproject.toml          # Project dependencies
├── .env.example
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) - Fast Python package installer (install with: `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd chatbot-rag
   ```

2. **Install dependencies with uv**:
   ```bash
   uv sync
   ```
   
   This will automatically create a virtual environment in `.venv` and install all dependencies.

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

### Running the Application

You need to run both the backend and frontend servers:

**Terminal 1 - Backend**:
```bash
cd backend
uv run python main.py
```
The backend will start on `http://localhost:8000`

**Terminal 2 - Frontend**:
```bash
cd frontend
uv run python app.py
```
The frontend will start on `http://localhost:7860`

Then open your browser and navigate to `http://localhost:7860`

## 📖 Usage

### Uploading Documents

1. Click on the **Upload Documents** section in the right panel
2. Select a supported file (PDF, DOCX, TXT, MD, XLSX, PPTX)
3. Click **Upload & Process**
4. Wait for confirmation that the document has been processed

### Chatting

1. Type your message in the text box at the bottom
2. Toggle **Use RAG** to search uploaded documents (enabled by default)
3. Click **Send** or press Enter
4. The chatbot will respond using context from your documents (if RAG is enabled)

### Managing Documents

- **List Documents**: Click to see all uploaded documents
- **Clear All Documents**: Remove all documents from the vector store
- **Clear Chat**: Clear the current conversation history

### Analytics

The bottom section shows real-time analytics:
- **Total Messages**: Number of messages exchanged
- **Files Uploaded**: Number of documents processed
- **RAG Queries**: Number of queries that used document retrieval
- **Activity Chart**: Message activity over time

## 🎨 UI Features

### Three.js Animations
- Animated particle system that responds to mouse movement
- Dynamic wave mesh with real-time deformation
- Gradient lighting effects

### D3.js Visualizations
- Real-time message activity chart
- Interactive statistics cards with animations
- Responsive and adaptive to screen size

### Modern Design
- Glassmorphism effect with backdrop blur
- Smooth transitions and animations
- Dark theme optimized for extended use
- Responsive layout for all screen sizes

## 🔧 Configuration

### Backend Configuration

Edit `backend/main.py` to customize:
- Vector store settings
- Chunk size and overlap
- Number of retrieved documents
- Model parameters

### Frontend Configuration

Edit `frontend/app.py` to customize:
- UI theme and colors
- Chart parameters
- Animation settings
- Default values

### Document Processing

Edit `backend/document_processor.py` to adjust:
- Chunk size (default: 1000 characters)
- Chunk overlap (default: 200 characters)
- Supported file types

## 📊 API Endpoints

### Backend API

- `GET /`: Health check
- `POST /upload`: Upload and process a document
- `POST /chat`: Send a chat message
- `GET /documents`: List all uploaded documents
- `DELETE /documents`: Clear all documents

### Request Examples

**Upload Document**:
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@document.pdf"
```

**Chat**:
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is this document about?",
    "use_rag": true
  }'
```

## 🛠️ Technologies Used

### Backend
- **FastAPI**: Modern, fast web framework
- **Google Gemini AI**: Advanced language model
- **ChromaDB**: Vector database for embeddings
- **LangChain**: RAG framework
- **Sentence Transformers**: Text embeddings

### Frontend
- **Gradio**: Python web UI framework
- **Three.js**: 3D graphics and animations
- **D3.js**: Data visualization
- **Custom CSS**: Glassmorphism design

### Document Processing
- **PyPDF**: PDF processing
- **python-docx**: Word document processing
- **openpyxl**: Excel file processing
- **python-pptx**: PowerPoint processing

## 🔍 Troubleshooting

### Backend won't start
- Check that port 8000 is not in use
- Verify GEMINI_API_KEY is set in .env file
- Ensure all dependencies are installed

### Frontend won't connect to backend
- Verify backend is running on port 8000
- Check API_URL in .env file
- Check firewall settings

### Document upload fails
- Ensure file format is supported
- Check file size (large files may take longer)
- Verify uploads/ directory exists and is writable

### No 3D animations showing
- Check browser console for JavaScript errors
- Ensure Three.js CDN is accessible
- Try a different browser (Chrome/Firefox recommended)

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgments

- Google Gemini AI for the powerful language model
- Gradio team for the amazing UI framework
- Three.js and D3.js communities for excellent documentation

## 📧 Support

For issues and questions, please open an issue on the GitHub repository.

---

**Built with ❤️ using Gemini AI, Gradio, FastAPI, Three.js, and D3.js**
