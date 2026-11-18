import os
import connect_with_db
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

db = connect_with_db

if not os.path.exists("tasks.db"):
    db.create_db_and_tables()
    db.count_rows()
db.count_rows()

class TaskCreate(BaseModel):
    title : str | None = None

task_objects = [
    { "id" : 1 , "title" : "surat al-kahf" , "done" : False},
    { "id" : 2 , "title" : "clean room" , "done" : False },
    { "id" : 3 , "title" : "eat breakfast" , "done" : True}
]

@app.get("/")
async def root():
    return { "name" : "Task API" , "version" : 1.0 , "endpoints" : ["/tasks"] }

@app.get("/health")
async def health():
    return { "status" : "ok" }

@app.get("/tasks")
async def task():
    return db.list_tasks()

@app.get("/tasks/{id}")
async def tasks_id(id : int):
    for task in db.list_tasks():
        if task.id == id:
            return db.list_tasks(id)
    raise HTTPException(status_code=404, detail = f"item {id} not found")

@app.post("/tasks", status_code=201)
async def add_task(task : TaskCreate, done :bool |None= None):
    if task.title is None or not task.title.strip():
         raise HTTPException(status_code=400, detail = "Title cannot be empty" )
    else:
        return db.create_tasks(task.title, done)
            

@app.put("/tasks/{id}")
async def update_task(id: int, title: str|None= None, done: bool | None = None):
    for task in db.list_tasks():
        if task.id == id:
           if title is None or not title.strip():
               raise HTTPException(status_code=400, detail= "Envalid/Empty Bady") 
           else:
               return db.update_tasks(id,title,done)
    raise HTTPException(status_code=404, detail= f"item {id} not found")      


@app.delete("/task/{id}", status_code=204)
async def delete_task(id: int):
    for task in db.list_tasks():
        if task.id == id:
            db.delete_tasks(id)
    raise HTTPException(status_code=404, detail= f"task {id} is not found")