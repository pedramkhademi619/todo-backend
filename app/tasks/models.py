from sqlalchemy import func, Integer, DateTime, ForeignKey
from sqlalchemy import Boolean, Column, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.users.models import UserModel

class TaskModel(Base):
    __tablename__ = "tasks"
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    title = Column(String(100), nullable=False)
    description = Column(Text(500), nullable=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())
    users = relationship("UserModel", back_populates="tasks", )

    def __repr__(self):
        return f"<Task {self.id}>, <title = {self.title}>, <description = {self.description}>, <is_completed = {self.is_completed}>, <created_at = {self.created_at}>, <updated_at = {self.updated_at}> "
