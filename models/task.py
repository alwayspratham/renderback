from sqlalchemy import Column,Integer,String,DateTime,Boolean,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
from db.database import Base

class Task(Base):
    __tablename__="tasks"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String(255),nullable=False)
    description=Column(String(300))
    is_completed=Column(Boolean,default=False)
    owner_id=Column(Integer,ForeignKey("user.id"),nullable=False)
    created_at=Column(DateTime,default=datetime.now(timezone.utc))

    owner=relationship("User",back_populates="tasks")
