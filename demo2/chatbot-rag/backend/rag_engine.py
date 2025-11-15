from typing import List, Tuple
import chromadb
from chromadb.config import Settings
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import uuid
from datetime import datetime
import os

class RAGEngine:
    """RAG engine for document retrieval and response generation"""

    def __init__(self, collection_name: str = "documents"):
        # Initialize ChromaDB
        self.client = chromadb.Client(Settings(
            anonymized_telemetry=False,
            allow_reset=True
        ))

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

        # Initialize embedding model
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

        # Initialize Gemini
        self.model = genai.GenerativeModel(os.getenv("GEMINI_MODEL"))

        # Session history
        self.session_history = {}

    def add_documents(self, chunks: List[str], source_name: str) -> str:
        """Add document chunks to vector store"""
        doc_id = str(uuid.uuid4())

        # Generate embeddings
        embeddings = self.embedder.encode(chunks).tolist()

        # Prepare metadata
        ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
        metadatas = [
            {
                "source": source_name,
                "doc_id": doc_id,
                "chunk_index": i,
                "timestamp": datetime.now().isoformat()
            }
            for i in range(len(chunks))
        ]

        # Add to collection
        self.collection.add(
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )

        return doc_id

    def retrieve_relevant_chunks(self, query: str, n_results: int = 5) -> Tuple[List[str], List[str]]:
        """Retrieve relevant chunks for a query"""
        # Generate query embedding
        query_embedding = self.embedder.encode([query]).tolist()

        # Query collection
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )

        if not results['documents'] or not results['documents'][0]:
            return [], []

        documents = results['documents'][0]
        sources = [meta.get('source', 'Unknown') for meta in results['metadatas'][0]]

        return documents, sources

    def generate_response(self, query: str, session_id: str, n_results: int = 5) -> Tuple[str, List[str]]:
        """Generate response using RAG"""
        # Retrieve relevant chunks
        relevant_chunks, sources = self.retrieve_relevant_chunks(query, n_results)

        # Get session history
        history = self.session_history.get(session_id, [])

        # Build context
        context = "\n\n".join(relevant_chunks) if relevant_chunks else ""

        # Build prompt
        if context:
            prompt = f"""You are a helpful AI assistant. Use the following context from the uploaded documents to answer the user's question. If the context doesn't contain relevant information, use your general knowledge but mention that the answer is not from the uploaded documents.

Context from documents:
{context}

Previous conversation:
{self._format_history(history)}

User question: {query}

Please provide a helpful and accurate response:"""
        else:
            prompt = f"""You are a helpful AI assistant. No specific documents have been uploaded yet, so please answer based on your general knowledge.

Previous conversation:
{self._format_history(history)}

User question: {query}

Please provide a helpful response:"""

        # Generate response
        response = self.model.generate_content(prompt)

        # Update session history
        history.append({"role": "user", "content": query})
        history.append({"role": "assistant", "content": response.text})
        self.session_history[session_id] = history[-10:]  # Keep last 10 messages

        # Get unique sources
        unique_sources = list(set(sources)) if sources else []

        return response.text, unique_sources

    def _format_history(self, history: List[dict]) -> str:
        """Format conversation history"""
        if not history:
            return "No previous conversation."

        formatted = []
        for msg in history[-6:]:  # Last 6 messages (3 exchanges)
            role = msg['role'].capitalize()
            content = msg['content']
            formatted.append(f"{role}: {content}")

        return "\n".join(formatted)

    def clear_all(self):
        """Clear all documents from collection"""
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection.name,
            metadata={"hnsw:space": "cosine"}
        )
        self.session_history = {}

    def list_documents(self) -> List[dict]:
        """List all documents in the collection"""
        try:
            results = self.collection.get()
            if not results['metadatas']:
                return []

            # Get unique documents
            docs = {}
            for metadata in results['metadatas']:
                doc_id = metadata.get('doc_id')
                if doc_id and doc_id not in docs:
                    docs[doc_id] = {
                        'doc_id': doc_id,
                        'source': metadata.get('source'),
                        'timestamp': metadata.get('timestamp')
                    }

            return list(docs.values())
        except Exception:
            return []
