from datetime import datetime
from enum import Enum
from app import db

# Enum class to represent task importance levels
class Importance(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

# Database model to represent a ToDo item
class ToDo(db.Model):
    # Unique identifier for each todo item
    id = db.Column(db.Integer, primary_key=True)
    # Content/description of the todo item
    content = db.Column(db.String(120), nullable=False)
    # Flag to indicate if the task is completed or not
    is_completed = db.Column(db.Boolean, default=False)
    # Flag to indicate if the task is deleted (soft delete)
    is_deleted = db.Column(db.Boolean, default=False)

    #Timestemp when the task was created
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    #Timestemp when the task was created
    update_time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    #Deadline for the task (can be null if no deadline)
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

