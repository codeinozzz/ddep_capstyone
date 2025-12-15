from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4
import json


class Message:
    def __init__(
        self,
        role: str,
        content: str,
        message_type: str = "text",
        metadata: Optional[Dict] = None,
    ):
        self.role = role
        self.content = content
        self.message_type = message_type
        self.metadata = metadata or {}
        self.timestamp = datetime.now().isoformat()

    def to_dict(self):
        return {
            "role": self.role,
            "content": self.content,
            "message_type": self.message_type,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
        }


class Session:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.messages: List[Message] = []
        self.config = {
            "style": "modern",
            "default_mode": "auto",
            "max_steps": 50,
            "guidance_scale": 7.5,
        }

    def add_message(self, message: Message):
        self.messages.append(message)
        self.last_activity = datetime.now()

    def get_history(self, limit: Optional[int] = None) -> List[Dict]:
        messages = self.messages[-limit:] if limit else self.messages
        return [msg.to_dict() for msg in messages]

    def update_config(self, updates: Dict):
        self.config.update(updates)

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "message_count": len(self.messages),
            "config": self.config,
        }


class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, Session] = {}

    def create_session(self) -> str:
        session_id = str(uuid4())
        self.sessions[session_id] = Session(session_id)
        return session_id

    def get_session(self, session_id: str) -> Optional[Session]:
        return self.sessions.get(session_id)

    def delete_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]

    def get_all_sessions(self) -> List[Dict]:
        return [session.to_dict() for session in self.sessions.values()]
