from sqlmodel import SQLModel, Field, create_engine,Session,select

class Tasks(SQLModel, table= True):
    id: int | None = Field(default=None, primary_key= True)
    title: str
    done:bool |None = Field(default=0)

sqlite_url = "sqlite:///tasks.db"
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():  
    SQLModel.metadata.create_all(engine) 

def create_tasks():
    task_1=Tasks(title="read azkar")
    task_2=Tasks(title="salah")
    task_3=Tasks(title="prepare a healthy meal")

    with Session(engine) as session:
        session.add(task_1)
        session.add(task_2)
        session.add(task_3) 

        session.commit()
        
def count_rows():
    with Session(engine) as session:
        statement= select(Tasks)
        results = session.exec(statement).all()
        
        if len(results) == 0:
            create_tasks()
    
if __name__ == "__main__":
    count_rows()