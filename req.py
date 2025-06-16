from models import engine, Task
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(autoflush=False,bind = engine)

def add_task(task_id,text,answer_options,type_answer,themes,img,created_at,updated_at):
    with Session(autoflush=False, bind=engine) as db:
        task = Task(task_id,text,answer_options,type_answer,themes,img,created_at,updated_at)
        db.add(task)
        db.commit()



