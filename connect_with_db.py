from sqlmodel import SQLModel, Field, create_engine,Session,select
from dotenv import load_dotenv
import os 

load_dotenv()

class Tasks(SQLModel, table= True):
    id: int | None = Field(default=None, primary_key= True)
    title: str
    done:bool |None = Field(default=0)

dburl= os.environ["DATABASE_URL"]
sqlite_url = "sqlite:///tasks.db"
engine = create_engine(dburl, echo=True)

def create_db_and_tables():  
    SQLModel.metadata.create_all(engine) 

def create_tasks(task :Tasks):
    with Session(engine) as session:
            new_task= Tasks(id= task.id,title= task.title,done=task.done)
            session.add(new_task)
            session.commit()
            task_result= session.get(Tasks, new_task.id)
            return task_result
        
def count_rows():
    with Session(engine) as session:
        if session.exec(select(Tasks)).first() is None:
            session.add_all(
                [
                    Tasks(id=1,title="untitled task 1"),
                    Tasks(id=2,title="untitled task 2"),
                    Tasks(id=3,title="untitled task 3")
                ]
            )
            session.commit()

def list_tasks(id : int | None = None):
    with Session(engine) as session:
        if id is not None:
            statement= select(Tasks).where(Tasks.id == id)
            result = session.exec(statement)
            return (result.one())
        if id is None:
            objects = session.exec(select(Tasks).order_by(Tasks.id))
            return (objects.all())

def update_tasks(id:int,title:str|None=None, done:bool|None=None):
    with Session(engine) as session:
        statement= select(Tasks).where(Tasks.id == id)
        result = session.exec(statement)
        task=result.one()
        if title is not None:
            task.title = title
        if done is not None:
            task.done = done
            
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
        


def delete_tasks(id:int):
    with Session(engine) as session:
        statement=select(Tasks).where(Tasks.id==id)
        result=session.exec(statement)
        task=result.one()
        session.delete(task)
        session.commit() 