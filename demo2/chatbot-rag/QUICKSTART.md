# 🚀 Quick Start Guide

## Step 1: Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

## Step 2: Set Up the Project

```bash
# Navigate to the project directory
cd chatbot-rag

# Copy the environment template
cp .env.example .env

# Edit .env and paste your API key
# Replace 'your_gemini_api_key_here' with your actual key
```

On **macOS/Linux**:
```bash
nano .env  # or use your favorite editor
```

On **Windows**:
```cmd
notepad .env
```

## Step 3: Install uv (if not already installed)

### macOS/Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Step 4: Install Dependencies

```bash
# This will create a virtual environment and install all dependencies
uv sync
```

## Step 5: Run the Application

### Option A: Using the Startup Script (Recommended)

**macOS/Linux**:
```bash
./start.sh
```

**Windows**:
```cmd
start.bat
```

### Option B: Manual Start (Two Terminals)

**Terminal 1 - Backend**:
```bash
cd backend
uv run python main.py
```

**Terminal 2 - Frontend**:
```bash
cd frontend
uv run python app.py
```

## Step 6: Access the Application

Open your browser and go to:
```
http://localhost:7860
```

## 🎉 You're Ready!

1. Upload a document (PDF, DOCX, TXT, etc.)
2. Wait for it to be processed
3. Start chatting with your document!

## 💡 Tips

- Keep "Use RAG" checked to search your uploaded documents
- Uncheck it to use general Gemini AI without document context
- The 3D background responds to your mouse movement
- View analytics at the bottom to see your chat activity

## ⚠️ Troubleshooting

### "Module not found" errors
```bash
uv sync
```

### Backend won't start
- Make sure port 8000 is not in use
- Check that your API key is correct in `.env`

### Frontend can't connect
- Make sure the backend is running first
- Check that both are running on localhost

### No animations showing
- Try refreshing the page
- Make sure JavaScript is enabled in your browser
- Use Chrome or Firefox for best results

## 🆘 Need Help?

Check the full README.md for detailed documentation and troubleshooting.
