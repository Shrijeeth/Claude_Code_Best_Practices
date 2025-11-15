import gradio as gr
import requests
from pathlib import Path
import os
from typing import List, Tuple

# Backend API URL
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Session ID for conversation continuity
session_id = None


def upload_file(file):
    """Upload file to backend"""
    if file is None:
        return "Please select a file to upload."

    try:
        files = {"file": open(file.name, "rb")}
        response = requests.post(f"{API_URL}/upload", files=files)

        if response.status_code == 200:
            result = response.json()
            return f"✅ Successfully uploaded: {result['filename']}\n📊 Processed {result['chunks_processed']} text chunks"
        else:
            return f"❌ Error: {response.json().get('detail', 'Upload failed')}"
    except Exception as e:
        return f"❌ Error uploading file: {str(e)}"


def chat(message: str, history: List[Tuple[str, str]], use_rag: bool):
    """Send message to chatbot"""
    global session_id

    if not message.strip():
        return history, ""

    try:
        # Add user message to history
        history = history + [(message, None)]

        # Prepare request
        payload = {
            "message": message,
            "session_id": session_id,
            "use_rag": use_rag
        }

        # Send to backend
        response = requests.post(f"{API_URL}/chat", json=payload)

        if response.status_code == 200:
            result = response.json()
            session_id = result["session_id"]

            bot_response = result["response"]

            # Add sources if available
            if result.get("sources"):
                sources_text = "\n\n📚 **Sources:** " + ", ".join(result["sources"])
                bot_response += sources_text

            # Update history with bot response
            history[-1] = (message, bot_response)

            return history, ""
        else:
            error_msg = f"Error: {response.json().get('detail', 'Request failed')}"
            history[-1] = (message, error_msg)
            return history, ""

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        history[-1] = (message, error_msg)
        return history, ""


def clear_documents():
    """Clear all documents from vector store"""
    try:
        response = requests.delete(f"{API_URL}/documents")
        if response.status_code == 200:
            return "✅ All documents cleared successfully"
        else:
            return f"❌ Error: {response.json().get('detail', 'Clear failed')}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def list_documents():
    """List all uploaded documents"""
    try:
        response = requests.get(f"{API_URL}/documents")
        if response.status_code == 200:
            docs = response.json().get("documents", [])
            if not docs:
                return "No documents uploaded yet."

            doc_list = "📁 **Uploaded Documents:**\n\n"
            for i, doc in enumerate(docs, 1):
                doc_list += f"{i}. {doc.get('source', 'Unknown')}\n"
            return doc_list
        else:
            return f"❌ Error: {response.json().get('detail', 'Request failed')}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


# Custom CSS and JavaScript
custom_head = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
"""

custom_js = ""

# Build the Gradio interface
with gr.Blocks(
    theme=gr.themes.Base(
        primary_hue="indigo",
        secondary_hue="pink",
    ),
    css=open("static/css/custom.css").read() if Path("static/css/custom.css").exists() else "",
    head=custom_head,
    title="AI Chatbot with RAG"
) as demo:
    # Header
    gr.HTML("""
        <div class="app-header">
            <h1 class="app-title">🤖 AI Chatbot with RAG</h1>
            <p class="app-subtitle">Chat with your documents using Gemini AI</p>
        </div>
    """)

    with gr.Row():
        with gr.Column(scale=2):
            # Chat Interface
            chatbot = gr.Chatbot(
                label="Chat",
                height=500,
                bubble_full_width=False,
                avatar_images=(None, "🤖"),
                show_copy_button=True,
            )

            with gr.Row():
                msg = gr.Textbox(
                    label="Message",
                    placeholder="Type your message here...",
                    show_label=False,
                    scale=4,
                    container=False
                )
                send_btn = gr.Button("Send 🚀", scale=1, variant="primary")

            with gr.Row():
                use_rag = gr.Checkbox(label="Use RAG (Search Documents)", value=True)
                clear_btn = gr.Button("Clear Chat 🗑️", size="sm")

        with gr.Column(scale=1):
            # File Upload Section
            gr.Markdown("### 📤 Upload Documents")
            file_upload = gr.File(
                label="Upload File",
                file_types=[".pdf", ".docx", ".txt", ".md", ".xlsx", ".pptx"],
                type="filepath"
            )
            upload_btn = gr.Button("Upload & Process", variant="primary")
            upload_status = gr.Textbox(
                label="Upload Status",
                interactive=False,
                show_label=False
            )

            gr.Markdown("---")

            # Document Management
            gr.Markdown("### 📚 Document Management")
            list_docs_btn = gr.Button("List Documents 📋")
            clear_docs_btn = gr.Button("Clear All Documents 🗑️", variant="stop")
            docs_status = gr.Textbox(
                label="Documents",
                interactive=False,
                show_label=False,
                lines=5
            )

    # Event handlers
    send_btn.click(
        chat,
        inputs=[msg, chatbot, use_rag],
        outputs=[chatbot, msg]
    )

    msg.submit(
        chat,
        inputs=[msg, chatbot, use_rag],
        outputs=[chatbot, msg]
    )

    upload_btn.click(
        upload_file,
        inputs=[file_upload],
        outputs=[upload_status]
    )

    clear_btn.click(
        lambda: ([], None),
        outputs=[chatbot, msg]
    )

    list_docs_btn.click(
        list_documents,
        outputs=[docs_status]
    )

    clear_docs_btn.click(
        clear_documents,
        outputs=[docs_status]
    )

    # Footer
    gr.HTML("""
        <div style="text-align: center; margin-top: 2rem; padding: 1rem; color: #94a3b8; font-size: 0.9rem;">
            <p>Powered by Gemini AI • Built with Gradio & FastAPI</p>
        </div>
    """)


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
