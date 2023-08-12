from datetime import datetime
from enum import Enum
from app import db

class Importance(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(120), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)

    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deadline = db.Column(db.DateTime, nullable=True)

    # Enum-based importance
    importance = db.Column(db.Enum(Importance), default=Importance.MEDIUM)

    # Return object data in easily serializeable format
    @property
    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'is_completed': self.is_completed,
            'is_deleted': self.is_deleted,
            'created_at': self.create_time.isoformat() if self.create_time else None,
            'updated_at': self.update_time.isoformat() if self.update_time else None,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'importance': self.importance.value if self.importance else None
        }

