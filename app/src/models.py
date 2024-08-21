from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime as dt

from .database import DatabaseInterface


Base = DatabaseInterface().get_declarative_base()


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=dt.now())
    updated_at = Column(DateTime, default=dt.now(), onupdate=dt.now())
    
    def __repr__(self):
        return f'<User {self.username}|{self.email} - {self.updated_at}>'