import json
import os
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class SessionManager:
    """Manages persistent storage of chat sessions"""

    def __init__(self, sessions_dir: str = "data/sessions"):
        """
        Initialize SessionManager

        Args:
            sessions_dir: Directory to store session files
        """
        self.sessions_dir = Path(sessions_dir)
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.sessions = {}
        self._load_all_sessions()

    def _load_all_sessions(self):
        """Load all existing sessions from disk"""
        try:
            for session_file in self.sessions_dir.glob("*.json"):
                session_id = session_file.stem
                try:
                    with open(session_file, 'r', encoding='utf-8') as f:
                        session_data = json.load(f)
                        self.sessions[session_id] = session_data.get('messages', [])
                        logger.info(f"Loaded session {session_id} with {len(self.sessions[session_id])} messages")
                except Exception as e:
                    logger.error(f"Error loading session {session_id}: {e}")

            logger.info(f"Loaded {len(self.sessions)} sessions from disk")
        except Exception as e:
            logger.error(f"Error loading sessions: {e}")

    def save_session(self, session_id: str, messages: List[Dict[str, str]]):
        """
        Save a session to disk

        Args:
            session_id: Unique session identifier
            messages: List of message dicts with 'role' and 'content' keys
        """
        try:
            session_file = self.sessions_dir / f"{session_id}.json"

            # Check if session exists to get created_at timestamp
            if session_file.exists():
                with open(session_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                    created_at = existing_data.get('created_at')
            else:
                created_at = datetime.now().isoformat()

            session_data = {
                'session_id': session_id,
                'created_at': created_at,
                'updated_at': datetime.now().isoformat(),
                'messages': messages,
                'message_count': len(messages)
            }

            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)

            # Update in-memory cache
            self.sessions[session_id] = messages
            logger.info(f"Saved session {session_id} with {len(messages)} messages")
        except Exception as e:
            logger.error(f"Error saving session {session_id}: {e}")
            raise

    def load_session(self, session_id: str) -> List[Dict[str, str]]:
        """
        Load a session from memory or disk

        Args:
            session_id: Unique session identifier

        Returns:
            List of message dicts, or empty list if session doesn't exist
        """
        # Check in-memory cache first
        if session_id in self.sessions:
            return self.sessions[session_id]

        # Try loading from disk
        session_file = self.sessions_dir / f"{session_id}.json"
        if session_file.exists():
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                    messages = session_data.get('messages', [])
                    self.sessions[session_id] = messages
                    return messages
            except Exception as e:
                logger.error(f"Error loading session {session_id}: {e}")

        return []

    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session from memory and disk

        Args:
            session_id: Unique session identifier

        Returns:
            True if session was deleted, False if it didn't exist
        """
        try:
            session_file = self.sessions_dir / f"{session_id}.json"

            # Remove from memory
            if session_id in self.sessions:
                del self.sessions[session_id]

            # Remove from disk
            if session_file.exists():
                session_file.unlink()
                logger.info(f"Deleted session {session_id}")
                return True

            return False
        except Exception as e:
            logger.error(f"Error deleting session {session_id}: {e}")
            raise

    def list_sessions(self) -> List[Dict]:
        """
        List all available sessions with metadata

        Returns:
            List of session metadata dicts
        """
        sessions_list = []

        try:
            for session_file in self.sessions_dir.glob("*.json"):
                try:
                    with open(session_file, 'r', encoding='utf-8') as f:
                        session_data = json.load(f)

                        # Get first user message as preview
                        preview = "No messages"
                        for msg in session_data.get('messages', []):
                            if msg.get('role') == 'user':
                                preview = msg.get('content', '')[:100]
                                if len(msg.get('content', '')) > 100:
                                    preview += "..."
                                break

                        sessions_list.append({
                            'session_id': session_data.get('session_id'),
                            'created_at': session_data.get('created_at'),
                            'updated_at': session_data.get('updated_at'),
                            'message_count': session_data.get('message_count', 0),
                            'preview': preview
                        })
                except Exception as e:
                    logger.error(f"Error reading session file {session_file}: {e}")

            # Sort by updated_at (most recent first)
            sessions_list.sort(key=lambda x: x.get('updated_at', ''), reverse=True)

        except Exception as e:
            logger.error(f"Error listing sessions: {e}")

        return sessions_list

    def clear_all_sessions(self):
        """Delete all sessions from memory and disk"""
        try:
            # Clear memory
            self.sessions = {}

            # Clear disk
            for session_file in self.sessions_dir.glob("*.json"):
                session_file.unlink()

            logger.info("Cleared all sessions")
        except Exception as e:
            logger.error(f"Error clearing sessions: {e}")
            raise

    def get_session_count(self) -> int:
        """Get total number of stored sessions"""
        return len(list(self.sessions_dir.glob("*.json")))

    def export_session(self, session_id: str) -> Optional[Dict]:
        """
        Export a session's full data

        Args:
            session_id: Unique session identifier

        Returns:
            Full session data dict or None if not found
        """
        session_file = self.sessions_dir / f"{session_id}.json"
        if session_file.exists():
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error exporting session {session_id}: {e}")

        return None
