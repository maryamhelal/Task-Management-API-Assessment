# Task Management API

## Setup Instructions

### Installation

```bash
pip install -r requirements.txt
```

### Run the application
Option 1 (seeds the database automatically, and runs the fastapi server): 
```bash
python main.py 
```
Option 2 (no automatic seeding, you have to manually run seed endpoint):
```bash
fastapi dev main.py 
```
Option 3 (using docker, with no automatic seeding, you have to manually run seed endpoint):
```bash
docker build -t task-management . ; docker run -it --rm -p 8000:8000 task-management
```

### API Access
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs) (for interactive documentation)
- ReDoc UI: [http://localhost:8000/redoc](http://localhost:8000/redoc) (for alternative documentation)
- OpenAPI JSON: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json) (for openapi schema)

### Testing
Run all unit tests using:
```bash
pytest
```

### Example API calls (using CMD and cURL)

#### Get all tasks
```bash
curl -X GET http://localhost:8000/tasks
```
#### Create a task
```bash
curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"title\": \"Sample Task\", \"priority\": \"high\"}"
```

#### Get a task using id
```bash
curl -X GET http://localhost:8000/tasks/1
```

#### Update a task using id
```bash
curl -X PUT http://localhost:8000/tasks/1 -H "Content-Type: application/json" -d "{\"description\": \"New description\", \"status\": \"completed\"}"
```

#### Delete a task using id
```bash
curl -X DELETE http://localhost:8000/tasks/1
```

#### Filter tasks using status
```bash
curl -X GET http://localhost:8000/tasks/status/pending
```

#### Filter tasks using priority
```bash
curl -X GET http://localhost:8000/tasks/priority/medium
```

#### Filter tasks using status and priority
```bash
curl -X GET http://localhost:8000/tasks/status/pending/priority/medium
```

#### Sort tasks by title ascendingly
```bash
curl -X GET http://localhost:8000/tasks/status/pending/priority/medium
```

#### Sort tasks by due_date ascendingly
```bash
curl -X GET http://localhost:8000/tasks/status/pending/priority/medium
```

#### Sort tasks by updated_at descendingly
```bash
curl -X GET http://localhost:8000/tasks/status/pending/priority/medium
```

#### Update tasks with status pending to be in_progress
```bash
curl -X GET http://localhost:8000/tasks/status/pending/priority/medium
```

#### Delete cancelled tasks
```bash
curl -X GET http://localhost:8000/tasks/status/pending/priority/medium
```

### Project Structure
- models.py: contains all models and enums needed for the SQLModel database and Pydantic
- database.py: creates the database connection and setup
- database_seeder.py: creates sample task records for testing
- main.py: contains the API endpoints and runs the application
- test_apis: tests all API endpoints using unit testing