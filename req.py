from models import engine, Task
from sqlalchemy.orm import sessionmaker
import os
import json
import logging
logger = logging.getLogger(__name__)

Session = sessionmaker(bind=engine)

def add_task(task_id, txt, question, answer_options, type_answer, themes, img):
    with Session() as db:
        existing_task = db.query(Task).filter_by(task_id=task_id).first()
        
        if existing_task:
            logger.debug(f"Задача с ID {task_id} уже существует, пропускаем")
            return False 
        
        
        if isinstance(answer_options, list):
            answer_options = json.dumps(answer_options, ensure_ascii=False)
        if isinstance(themes, list):
            themes = json.dumps(themes, ensure_ascii=False)
        
        addtask = Task(
            task_id=task_id,
            task=question,
            text=txt,
            answer_options=answer_options,
            type_answer=type_answer,
            themes=themes,
            img=img
        )
        
        db.add(addtask)
        db.commit()
        logger.debug(f"{task_id} added")



def check_database_data(db_path="tasks.db"):
    if not os.path.exists(db_path):
        return 0
    try:
        with Session() as session:
            count = session.query(Task).count()  
            logging.debug(f"Всего записей в таблице: {count}")
            return count
    except Exception as e:
        logger.warning(f"Ошибка при подсчете записей: {e}")
        return 0
