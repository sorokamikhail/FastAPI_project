# Project Title
ToDo List API
A simple RESTful API for managing a To-Do list, built with FastAPI and SQLite. This project demonstrates CRUD operations, asynchronous programming patterns, data validation, and automated testing.
## Requirements
- Python 3.9 or higher
- pip (Python package installer)
## Features

- List all tasks
- Retrieve a task by its ID
- Create new tasks
- Update existing tasks
- Delete tasks
- Request data validation with Pydantic
- Persistent storage using SQLite
- Automated tests for each endpoint

## Run Locally

Clone the project

```bash
  git clone https://github.com/sorokamikhail/FastAPI_project
```

Go to the project directory

```bash
  cd FastAPI_project
```

Install dependencies

```bash
  pip install fastapi uvicorn sqlalchemy pydantic pytest httpx
```

Start the server

```bash
  uvicorn app:app --reload
```
- The API will be accessible at http://127.0.0.1:8000

