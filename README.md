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
Option 2 (no automatic seeding, have to manually run seed endpoint):
```bash
fastapi dev main.py 
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
```bash
# Get all tasks
curl -X GET http://localhost:8000/tasks

# Create a task
curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"title\": \"Sample Task\", \"priority\": \"high\"}"

# Get a task using id
curl -X GET http://localhost:8000/tasks/1

# Update a task using id
curl -X PUT http://localhost:8000/tasks/1 -H "Content-Type: application/json" -d "{\"description\": \"New description\", \"status\": \"completed\"}"

# Delete a task using id
curl -X DELETE http://localhost:8000/tasks/1

# Filter tasks using status
curl -X GET http://localhost:8000/tasks/status/pending

# Filter tasks using priority
curl -X GET http://localhost:8000/tasks/priority/medium

# Filter tasks using status and priority
curl -X GET http://localhost:8000/tasks/status/pending/priority/medium
```

### Project Structure
- models.py: contains all models and enums needed for the SQLModel database and Pydantic
- database.py: creates the database connection and setup
- database_seeder.py: creates sample task records for testing
- main.py: contains the api endpoints and runs the application
- test_apis: tests all API endpoints using unit testing