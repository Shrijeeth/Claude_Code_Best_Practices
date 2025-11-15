#!/bin/bash

# Startup script for Chatbot RAG application

echo "🚀 Starting Chatbot RAG Application..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please copy .env.example to .env and add your Gemini API key"
    exit 1
fi

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ Error: uv is not installed!"
    echo "Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Install dependencies with uv (creates .venv automatically)
echo "📥 Installing dependencies with uv..."
uv sync

# Create necessary directories
mkdir -p uploads data logs

# Start backend in background
echo "🔌 Starting FastAPI backend on port 8000..."
cd backend
uv run python main.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to be ready..."
sleep 20

# Start frontend
echo "🎨 Starting Gradio frontend on port 7860..."
cd frontend
uv run python app.py

# Cleanup on exit
trap "kill $BACKEND_PID" EXIT
