import sys
import os

sys.path.append(os.path.dirname(__file__))

from fastapi.testclient import TestClient
import pytest
from main import app
from database import sqlite_file_name, engine

client = TestClient(app)

# 1. Test seeding
def test_seeding_returns_success():
    response = client.post("/seed")
    assert response.status_code == 201

# 2. Test get endpoints
def test_get_endpoints_returns_success():
    response = client.get("/")
    assert response.status_code == 200

# 3. Test get health status
def test_get_health_returns_success():
    response = client.get("/health")
    assert response.status_code == 200

# 4. Test create task with correct input
def test_post_tasks_returns_success():
    response = client.post(
        "/tasks",
        json={
            "title": "string", 
            "description": "string",
            "due_date": "2025-08-30T05:02:21.437Z",
            "assigned_to": "string"})
    assert response.status_code == 201

# 5. Test create task with incorrect input (empty title)
def test_post_tasks_empty_title_returns_validation_error():
    response = client.post(
        "/tasks",
        json={"title": ""})
    assert response.status_code == 422

# 6. Test create task with incorrect input (only whitespaced title)
def test_post_tasks_whitespaced_title_returns_validation_error():
    response = client.post(
        "/tasks",
        json={"title": " "})
    assert response.status_code == 422

# 7. Test create task with incorrect input (due date with a past date)
def test_post_tasks_past_due_date_returns_validation_error():
    response = client.post(
        "/tasks",
        json={"title": "Test Task", "due_date": "2024-02-05T02:04:56.916Z"})
    assert response.status_code == 422

# 8. Test get tasks
def test_get_tasks_returns_success():
    response = client.get("/tasks")
    assert response.status_code == 200

# 9. Test get task with correct id
def test_get_task_with_id_returns_success():
    response = client.get("/tasks/1")
    assert response.status_code == 200

# 10. Test get task with no task corresponding to id
def test_get_task_with_id_returns_not_found_error():
    response = client.get("/tasks/400")
    assert response.status_code == 404

# 11. Test get task with incorrect format of id
def test_get_task_with_id_returns_validation_error():
    response = client.get("/tasks/string")
    assert response.status_code == 422

# 12. Test update task with correct id
def test_put_task_with_id_returns_success():
    response = client.put("/tasks/1", json={"assigned_to": "John"})
    assert response.status_code == 200

# 13. Test update task with incorrect title
def test_put_task_with_id_returns_validation_error():
    response = client.put("/tasks/1", json={"title": ""})
    assert response.status_code == 422

# 14. Test update task with incorrect id
def test_put_task_with_id_returns_not_found_error():
    response = client.put("/tasks/720", json={"title": "New"})
    assert response.status_code == 404

# 15. Test delete task with correct id
def test_delete_task_with_id_returns_success():
    response = client.delete("/tasks/2")
    assert response.status_code == 200

# 16. Test delete task with incorrect id
def test_delete_task_with_id_returns_not_found_error():
    response = client.delete("/tasks/200")
    assert response.status_code == 404

# 17. Test filter tasks using status with correct input
def test_get_tasks_with_status_returns_success():
    response = client.get("/tasks/status/pending")
    assert response.status_code == 200

# 18. Test filter tasks using status with incorrect input
def test_get_tasks_with_status_returns_validation_error():
    response = client.get("/tasks/status/pen")
    assert response.status_code == 422

# 19. Test filter tasks using status to return empty array
def test_get_tasks_with_status_returns_empty_array():
    response = client.get("/tasks/status/in_progress")
    assert response.status_code == 200
    assert response.json() == []

# 20. Test filter tasks using priority with correct input
def test_get_tasks_with_priority_returns_success():
    response = client.get("/tasks/priority/medium")
    assert response.status_code == 200

# 21. Test filter tasks using priority with incorrect input
def test_get_tasks_with_priority_returns_validation_error():
    response = client.get("/tasks/priority/hi")
    assert response.status_code == 422

# 22. Test filter tasks using priority returns empty array
def test_get_tasks_with_priority_returns_empty_array():
    response = client.get("/tasks/priority/high")
    assert response.status_code == 200
    assert response.json() == []

# 23. Test filter tasks using status and priority with correct input
def test_get_tasks_with_status_and_priority_returns_success():
    response = client.get("/tasks/status/pending/priority/medium")
    assert response.status_code == 200

# 24. Test filter tasks using status and priority with incorrect input
def test_get_tasks_with_status_and_priority_returns_validation_error():
    response = client.get("/tasks/status/prog/priority/med")
    assert response.status_code == 422

# 25. Test filter tasks using status and priority returns empty array
def test_get_tasks_with_status_and_priority_returns_empty_array():
    response = client.get("/tasks/status/completed/priority/low")
    assert response.status_code == 200
    assert response.json() == []

# 26. Test get tasks sorted by title ascendingly
def test_get_tasks_sort_by_title_returns_success():
    response = client.get("/tasks/sortBy/title")
    print(response.json())
    assert response.status_code == 200

# 27. Test get tasks sorted by due date ascendingly
def test_get_tasks_sort_by_due_date_returns_success():
    response = client.get("/tasks/sortBy/dueDate")
    print(response.json())
    assert response.status_code == 200

# 28. Test get tasks sorted by updated at descendingly
def test_get_tasks_sort_by_updated_at_returns_success():
    response = client.get("/tasks/sortBy/updatedAt")
    print(response.json())
    assert response.status_code == 200

# Delete database after tests are done
@pytest.fixture(scope="session", autouse=True)
def cleanup_database_after_tests():
    yield
    engine.dispose()
    if os.path.exists(sqlite_file_name):
        os.remove(sqlite_file_name)