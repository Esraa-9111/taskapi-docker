from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

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
    return task_objects

@app.get("/tasks/{id}")
async def tasks_id(id : int):
    for task in task_objects:
        if task["id"] == id:
            return task
    raise HTTPException(status_code=404, detail = f"item {id} not found")

@app.post("/tasks", status_code=201)
async def add_task(task : TaskCreate):
    if task.title is None or not task.title.strip():
         raise HTTPException(status_code=400, detail = "Title cannot be empty" )
    else:
        new_id = max((object["id"] for object in task_objects), default=0) + 1
        new_task = {"id" : new_id, "title" : task.title, "done" : False}
        task_objects.append(new_task)
    return new_task
              

@app.put("/tasks/{id}")
async def update_task(id: int, title: str|None= None, done: bool | None = None):
    for task in task_objects:
        if task["id"] == id:
           if title is None or not title.strip():
               raise HTTPException(status_code=400, detail= "Envalid/Empty Bady") 
           else:
               task["title"] = title
               if done is not None:
                   task["done"] = done
               return task
    raise HTTPException(status_code=404, detail= f"item {id} not found")      


@app.delete("/task/{id}", status_code=204)
async def delete_task(id: int):
    for task in task_objects:
        if task['id'] == id:
            task_objects.remove(task)
            return task
        raise HTTPException(status_code=404, detail= f"task {id} is not found")