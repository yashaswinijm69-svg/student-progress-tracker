from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, ForeignKey, func
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

# Category CRUD Operations
def add_category(name, weekly_target_hours):
    session = get_session()
    try:
        clean_name = name.strip()
        existing = session.query(Category).filter(func.lower(Category.name) == clean_name.lower()).first()
        if existing:
            return False, f"Category '{clean_name}' already exists."
            
        new_category = Category(name=clean_name, weekly_target_hours=weekly_target_hours)
        session.add(new_category)
        session.commit()
        return True, "Category added successfully!"
    except Exception as e:
        session.rollback()
        return False, str(e)
    finally:
        session.close()

def get_all_categories():
    session = get_session()
    try:
        return session.query(Category).all()
    finally:
        session.close()

def update_category(category_id, name, weekly_target_hours):
    session = get_session()
    try:
        clean_name = name.strip()
        existing = session.query(Category).filter(
            func.lower(Category.name) == clean_name.lower(),
            Category.id != category_id
        ).first()
        if existing:
            return False, f"Category '{clean_name}' already exists."

        category = session.query(Category).filter(Category.id == category_id).first()
        if category:
            category.name = clean_name
            category.weekly_target_hours = weekly_target_hours
            session.commit()
            return True, "Category updated successfully!"
        return False, "Category not found."
    except Exception as e:
        session.rollback()
        return False, str(e)
    finally:
        session.close()

def delete_category(category_id):
    session = get_session()
    try:
        category = session.query(Category).filter(Category.id == category_id).first()
        if category:
            session.delete(category)
            session.commit()
            return True, "Category deleted successfully!"
        return False, "Category not found."
    except Exception as e:
        session.rollback()
        return False, str(e)
    finally:
        session.close()
