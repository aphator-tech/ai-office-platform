from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
import json

from app.models import UserPreference, Conversation, Message, Task


class MemoryService:
    """Service for managing user memory and preferences."""
    
    def __init__(self, db: Session):
        self.db = db
    
    # User Preferences
    def get_preference(self, user_id: str, key: str) -> Optional[Any]:
        """Get a user preference."""
        pref = self.db.query(UserPreference).filter(
            UserPreference.user_id == user_id,
            UserPreference.key == key
        ).first()
        return pref.value if pref else None
    
    def set_preference(self, user_id: str, key: str, value: Dict[str, Any]) -> UserPreference:
        """Set a user preference."""
        existing = self.db.query(UserPreference).filter(
            UserPreference.user_id == user_id,
            UserPreference.key == key
        ).first()
        
        if existing:
            existing.value = value
            existing.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(existing)
            return existing
        else:
            pref = UserPreference(
                user_id=user_id,
                key=key,
                value=value
            )
            self.db.add(pref)
            self.db.commit()
            self.db.refresh(pref)
            return pref
    
    def get_all_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get all preferences for a user."""
        prefs = self.db.query(UserPreference).filter(
            UserPreference.user_id == user_id
        ).all()
        return {p.key: p.value for p in prefs}
    
    # Conversation History
    def get_conversation_history(
        self, 
        user_id: str, 
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get user's conversation history."""
        conversations = self.db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).order_by(Conversation.updated_at.desc()).limit(limit).all()
        
        return [
            {
                "id": c.id,
                "title": c.title,
                "created_at": c.created_at.isoformat(),
                "updated_at": c.updated_at.isoformat()
            }
            for c in conversations
        ]
    
    def get_conversation_messages(
        self, 
        conversation_id: str
    ) -> List[Dict[str, Any]]:
        """Get all messages in a conversation."""
        messages = self.db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc()).all()
        
        return [
            {
                "id": m.id,
                "role": m.role,
                "agent_type": m.agent_type,
                "content": m.content,
                "metadata": m.metadata,
                "created_at": m.created_at.isoformat()
            }
            for m in messages
        ]
    
    # Task History
    def get_task_history(
        self, 
        conversation_id: Optional[str] = None,
        agent_type: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get task history with optional filters."""
        query = self.db.query(Task)
        
        if conversation_id:
            query = query.filter(Task.conversation_id == conversation_id)
        if agent_type:
            query = query.filter(Task.agent_type == agent_type)
        
        tasks = query.order_by(Task.created_at.desc()).limit(limit).all()
        
        return [
            {
                "id": t.id,
                "conversation_id": t.conversation_id,
                "agent_type": t.agent_type,
                "title": t.title,
                "status": t.status,
                "progress": t.progress,
                "created_at": t.created_at.isoformat(),
                "completed_at": t.completed_at.isoformat() if t.completed_at else None
            }
            for t in tasks
        ]
    
    # Search
    def search_conversations(
        self, 
        user_id: str, 
        query: str
    ) -> List[Dict[str, Any]]:
        """Search conversations by title or content."""
        conversations = self.db.query(Conversation).filter(
            Conversation.user_id == user_id,
            Conversation.title.ilike(f"%{query}%")
        ).all()
        
        results = []
        for c in conversations:
            # Also check messages
            messages = self.db.query(Message).filter(
                Message.conversation_id == c.id,
                Message.content.ilike(f"%{query}%")
            ).all()
            
            if messages or query.lower() in c.title.lower():
                results.append({
                    "id": c.id,
                    "title": c.title,
                    "matched_in": "title" if query.lower() in c.title.lower() else "messages",
                    "created_at": c.created_at.isoformat()
                })
        
        return results
    
    # Cleanup
    def clear_old_conversations(self, user_id: str, days: int = 30):
        """Clear conversations older than specified days."""
        from datetime import timedelta
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        conversations = self.db.query(Conversation).filter(
            Conversation.user_id == user_id,
            Conversation.created_at < cutoff
        ).all()
        
        for c in conversations:
            # Delete related messages and tasks
            self.db.query(Message).filter(Message.conversation_id == c.id).delete()
            self.db.query(Task).filter(Task.conversation_id == c.id).delete()
            self.db.delete(c)
        
        self.db.commit()
        
        return len(conversations)
