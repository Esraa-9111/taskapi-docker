import os
import connect_with_db as db
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app:FastAPI):
    db.create_db_and_tables()
    db.count_rows()
    yield

app = FastAPI(lifespan=lifespan)


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
async def add_task(task : str| None , done:bool|None=False):
    id_list=[]
    for t in db.list_tasks():
        id_list.append(t.id)
    last_id = max(id_list, default=0)
    if task is None or not task.strip():
         raise HTTPException(status_code=400, detail = "Title cannot be empty" )
    else:
        new_id = last_id+1
        new_task=db.Tasks(id=new_id, title=task,done=done)
        return db.create_tasks(new_task)

@app.put("/tasks/{id}")
async def update_task(id: int, title: str|None = None, done: bool | None = None):
    for task in db.list_tasks():
        if task.id == id:
           if title is not None or done is not None:
               return db.update_tasks(id,title,done)
           raise HTTPException(status_code=400, detail= "At least one of 'title' or 'done' must be provided")
    raise HTTPException(status_code=404, detail= f"item {id} not found")      


@app.delete("/task/{id}", status_code=204)
async def delete_task(id: int):
    id_list=[]
    for task in db.list_tasks():
        id_list.append(task.id)
    if id not in id_list:
        raise HTTPException(status_code=404, detail= f"task {id} is not found")
    db.delete_tasks(id)