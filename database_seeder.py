from models import Task, TaskStatus, TaskPriority
from datetime import datetime, timezone
from database import engine
from sqlmodel import Session

# Create different tasks
def create_tasks(): 
    task_1 = Task(title="Task 1", description="This is the first task")
    task_2 = Task(title="Task 2", description="This is the second task", priority=TaskPriority.urgent)
    task_3 = Task(title="string", status=TaskStatus.cancelled)
    task_4 = Task(title="Task 4", description="string", due_date=datetime.fromisoformat("2025-08-30T04:56:46.161+00:00").astimezone(timezone.utc))
    task_5 = Task(title="Task 5", assigned_to="Mohamed")
    
    with Session(engine) as session:
        session.add_all([task_1, task_2, task_3, task_4, task_5])
        session.commit()