import sys
import os

sys.path.append(os.path.dirname(__file__))

from models import *
from database import engine, create_db, sqlite_file_name
from database_seeder import create_tasks
from sqlmodel import Session, select
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import uvicorn

# API Endpoints
app = FastAPI()

# Create database and different tasks
@app.post("/seed")
async def seeder():
    main()
    return JSONResponse(status_code=201, content="Database seeded")

# Get all endpoints
@app.get("/")
def root():
    return{"endpoints": ["/health", "/tasks", "/seed"]}

# Get health status
@app.get("/health")
def health():
    return{"status": "OK"}

# Create a task
@app.post("/tasks")
async def create_task(task: TaskCreate):
    try:
        task_data = Task(**task.model_dump())
        with Session(engine) as session:
            session.add(task_data)
            session.commit()
            session.refresh(task_data)
            response = TaskResponse.model_validate(task_data, from_attributes=True).model_dump(mode="json")
            return JSONResponse(status_code=201, content=response)
    except ValidationError as e:
        raise HTTPException(status_code = 422, detail = str(e))
    except Exception as e:
        raise HTTPException(status_code = 400, detail = "An error occured, try again")

# Get all tasks
@app.get("/tasks")
def get_tasks():
    try:
        with Session(engine) as session:
            statement = select(Task).offset(0)
            tasks = session.exec(statement).all()
            response = [TaskResponse.model_validate(task, from_attributes=True).model_dump(mode="json") for task in tasks]
            return JSONResponse(status_code=200, content=response)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = "An error occured, try again")

# Get a specific task with id
@app.get("/tasks/{task_id}")
def get_task_with_id(task_id: int):
    try:
        with Session(engine) as session:
            task = session.get(Task, task_id)
            if not task:
                raise HTTPException(status_code = 404, detail = "Task not found")
            response = TaskResponse.model_validate(task, from_attributes=True).model_dump(mode="json")
            return JSONResponse(status_code=200, content=response)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code = 400, detail = "An error occured, try again")

# Update a specific task with id
@app.put("/tasks/{task_id}")
async def update_task_with_id(task_id: int, tasknew: TaskUpdate):
    try:
        with Session(engine) as session:
            task = session.get(Task, task_id)
            if not task:
                raise HTTPException(status_code = 404, detail = "Task not found")
            if(tasknew.title):
                task.title = tasknew.title
            if(tasknew.description):
                task.description = tasknew.description
            if(tasknew.status):
                task.status = tasknew.status
            if(tasknew.priority):
                task.priority = tasknew.priority
            if(tasknew.due_date):
                task.due_date = tasknew.due_date
            if(tasknew.assigned_to):
                task.assigned_to = tasknew.assigned_to

            task.updated_at = datetime.now()
            session.add(task)
            session.commit()
            session.refresh(task)
            response = TaskResponse.model_validate(task, from_attributes=True).model_dump(mode="json")
            return JSONResponse(status_code=200, content=response)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code = 400, detail = "An error occured, try again")
    
# Delete a specific task with id
@app.delete("/tasks/{task_id}")
def delete_task_with_id(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code = 404, detail = "Task not found")
        session.delete(task)
        session.commit()

        task = session.get(Task, task_id)
        if(not task):
            return JSONResponse(status_code=200, content="Task deleted successfully")
        else:
            raise HTTPException(status_code = 400, detail = "Could not delete task")

# Filter tasks based on status
@app.get("/tasks/status/{status}")
def get_tasks_with_status(status: TaskStatus):
    try:
        with Session(engine) as session:
            statement = select(Task).where(Task.status == status)
            tasks = session.exec(statement).all()
            response = [TaskResponse.model_validate(task, from_attributes=True).model_dump(mode="json") for task in tasks]
            return JSONResponse(status_code=200, content=response)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = "An error occured, try again")    

# Filter tasks based on priority
@app.get("/tasks/priority/{priority}")
def get_tasks_with_priority(priority: TaskPriority):
    try:
        with Session(engine) as session:
            statement = select(Task).where(Task.priority == priority)
            tasks = session.exec(statement).all()
            response = [TaskResponse.model_validate(task, from_attributes=True).model_dump(mode="json") for task in tasks]
            return JSONResponse(status_code=200, content=response)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = "An error occured, try again")

# Filter tasks based on both status and priority
@app.get("/tasks/status/{status}/priority/{priority}")
def get_tasks_with_status_and_priority(status: TaskStatus, priority: TaskPriority):
    try:
        with Session(engine) as session:
            statement = select(Task).where(Task.status == status, Task.priority == priority).limit(10) # Shows only 10 records
            tasks = session.exec(statement).all()
            response = [TaskResponse.model_validate(task, from_attributes=True).model_dump(mode="json") for task in tasks]
            return JSONResponse(status_code=200, content=response)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = "An error occured, try again")  
    
# Sort tasks by ascending task title
@app.get("/tasks/sortBy/title")
def get_tasks_sorted_with_title():
    try:
        with Session(engine) as session:
            statement = select(Task).order_by(Task.title.asc())
            tasks = session.exec(statement).all()
            response = [TaskResponse.model_validate(task, from_attributes=True).model_dump(mode="json") for task in tasks]
            return JSONResponse(status_code=200, content=response)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = "An error occured, try again")

# Sort tasks by ascending due date
@app.get("/tasks/sortBy/dueDate")
def get_tasks_sorted_with_due_date():
    try:
        with Session(engine) as session:
            statement = select(Task).order_by(Task.due_date.asc())
            tasks = session.exec(statement).all()
            response = [TaskResponse.model_validate(task, from_attributes=True).model_dump(mode="json") for task in tasks]
            return JSONResponse(status_code=200, content=response)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = "An error occured, try again")
    
# Sort tasks by descending due date
@app.get("/tasks/sortBy/updatedAt")
def get_tasks_sorted_with_updated_at():
    try:
        with Session(engine) as session:
            statement = select(Task).order_by(Task.updated_at.desc())
            tasks = session.exec(statement).all()
            response = [TaskResponse.model_validate(task, from_attributes=True).model_dump(mode="json") for task in tasks]
            return JSONResponse(status_code=200, content=response)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = "An error occured, try again")
    
# Update pending tasks to be in progess
@app.put("/tasks/updateAll/pending")
def update_tasks_with_pending_status():
    try:
        with Session(engine) as session:
            statement = select(Task).where(Task.status == TaskStatus.pending)
            tasks = session.exec(statement).all()
            for task in tasks:
                task.status = TaskStatus.in_progress
                session.add(task)
            session.commit()
            for task in tasks:
                session.refresh(task)
            response = [TaskResponse.model_validate(task, from_attributes=True).model_dump(mode="json") for task in tasks]
            return JSONResponse(status_code=200, content=response)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = "An error occured, try again")  
    
# Delete cancelled tasks
@app.delete("/tasks/deleteAll/cancelled")
def delete_tasks_with_cancelled_status():
    try:
        with Session(engine) as session:
            statement = select(Task).where(Task.status == TaskStatus.cancelled)
            tasks = session.exec(statement).all()
            for task in tasks:
                session.delete(task)
            session.commit()
            return JSONResponse(status_code=200, content="Cancelled tasks deleted successfully")
    except Exception as e:
        raise HTTPException(status_code = 400, detail = "An error occured, try again")  
    
# Search in title and description
@app.get("/tasks/search/{text}")
def get_tasks_with_search_words(text: str):
    try:
        with Session(engine) as session:
            statement = select(Task).where(Task.title.contains(text) | Task.description.contains(text))
            tasks = session.exec(statement).all()
            response = [TaskResponse.model_validate(task, from_attributes=True).model_dump(mode="json") for task in tasks]
            return JSONResponse(status_code=200, content=response)
    except Exception as e:
        raise HTTPException(status_code = 400, detail = "An error occured, try again")

# Delete old database if exists, and create database and sample data
def main(): 
    engine.dispose()
    if os.path.exists(sqlite_file_name):
        os.remove(sqlite_file_name)
    create_db()
    create_tasks()

# For running the application, call main method and run fastapi
if __name__=="__main__":
    main()
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)