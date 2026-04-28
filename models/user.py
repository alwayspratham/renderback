from sqlalchemy import Column,Integer,String,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime,timezone

from db.database import Base


class User(Base):
    __tablename__="user"
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String(255),unique=True,nullable=False,index=True)
    password=Column(String(255),nullable=False)
    role=Column(String(255),default="user",nullable=False)
    created_at=Column(DateTime,default=datetime.now(timezone.utc))

    tasks=relationship("Task",back_populates="owner",cascade="all,delete")

