from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Define the database URL
DB_URL = "sqlite:///tracker.db"

Base = declarative_base()

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    weekly_target_hours = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    tasks = relationship("Task", back_populates="category")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    title = Column(String, nullable=False)
    is_habit = Column(Boolean, default=False)
    target_frequency = Column(String, nullable=True)
    deadline = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    category = relationship("Category", back_populates="tasks")
    completions = relationship("Completion", back_populates="task")

class Completion(Base):
    __tablename__ = 'completions'
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    date = Column(Date, nullable=False)
    completed = Column(Boolean, default=False)
    minutes_spent = Column(Integer, default=0)
    
    task = relationship("Task", back_populates="completions")

class Setting(Base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=True)
    notify_enabled = Column(Boolean, default=False)

def init_db():
    from sqlalchemy import create_engine
    engine = create_engine(DB_URL)
    Base.metadata.create_all(engine)
    return engine

def get_session():
    from sqlalchemy import create_engine
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    return Session()
