@echo off
REM Startup script for Chatbot RAG application (Windows)

echo 🚀 Starting Chatbot RAG Application...

REM Check if .env file exists
if not exist .env (
    echo ❌ Error: .env file not found!
    echo Please copy .env.example to .env and add your Gemini API key
    exit /b 1
)

REM Check if uv is installed
where uv >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Error: uv is not installed!
    echo Install it with: powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 ^| iex"
    exit /b 1
)

REM Install dependencies with uv (creates .venv automatically)
echo 📥 Installing dependencies with uv...
uv sync

REM Create necessary directories
if not exist uploads mkdir uploads
if not exist data mkdir data
if not exist logs mkdir logs

REM Start backend in new window
echo 🔌 Starting FastAPI backend on port 8000...
start "Backend Server" cmd /k "cd backend && uv run python main.py"

REM Wait for backend to start
echo ⏳ Waiting for backend to be ready...
timeout /t 5 /nobreak

REM Start frontend
echo 🎨 Starting Gradio frontend on port 7860...
cd frontend
uv run python app.py
