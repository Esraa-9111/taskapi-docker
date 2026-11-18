from sqlmodel import SQLModel, Field, create_engine,Session,select

class Tasks(SQLModel, table= True):
    id: int | None = Field(default=None, primary_key= True)
    title: str
    done:bool |None = Field(default=0)

sqlite_url = "sqlite:///tasks.db"
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():  
    SQLModel.metadata.create_all(engine) 

def create_tasks(titlex :str | None = None, donex:bool|None=None):
    task_1=Tasks(title="untitled 1")
    task_2=Tasks(title="untitled 2")
    task_3=Tasks(title="untitled 3")

    with Session(engine) as session:
        if titlex is None:
            session.add(task_1)
            session.add(task_2)
            session.add(task_3)
            session.commit() 
        else:
            taskx= Tasks(title= titlex, done= donex)
            session.add(taskx)
            session.commit()
            task = session.get(Tasks, taskx.id)
            return task
        
def count_rows():
    with Session(engine) as session:
        statement= select(Tasks)
        results = session.exec(statement).all()
        
        if len(results) == 0:
            create_tasks()

def list_tasks(id : int | None = None):
    with Session(engine) as session:
        if id is not None:
            statement= select(Tasks).where(Tasks.id == id)
            result = session.exec(statement)
            return (result.one())
        if id is None:
            objects = session.exec(select(Tasks))
            return (objects.all())

def update_tasks(id:int,title:str|None=None, done:bool|None=None):
    with Session(engine) as session:
        statement= select(Tasks).where(Tasks.id == id)
        result = session.exec(statement)
        task=result.one()
        if title or done is not None:
            task.title = title
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