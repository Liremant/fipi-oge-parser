from models import engine, Task
from sqlalchemy.orm import sessionmaker
import json

Session = sessionmaker(bind=engine)

def add_task(task_id, text,question, answer_options, type_answer, themes, img):
    with Session() as db:
        # Преобразуем список в строку, если это список
        if isinstance(answer_options, list):
            answer_options_str = json.dumps(answer_options, ensure_ascii=False)
        else:
            answer_options_str = answer_options
        atask = Task(
            task_id=task_id,
            task=question,
            text=text,
            answer_options=answer_options_str,  # строка вместо списка
            type_answer=type_answer,
            themes=themes,
            img=img
        )
        db.add(atask)
        db.commit()