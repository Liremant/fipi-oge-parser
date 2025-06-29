from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import  create_engine, Column, Integer, String, Text, DateTime, func
engine = create_engine("sqlite:///tasks.db",echo=False)


class Base(DeclarativeBase): 
    pass

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(20), unique=True, nullable=False, index=True)
    task = Column(Text)
    text = Column(Text, nullable=False)
    answer_options = Column(Text)
    type_answer = Column(String(100), nullable=False)
    themes = Column(String(500))
    img = Column(Text)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


Base.metadata.create_all(bind=engine)