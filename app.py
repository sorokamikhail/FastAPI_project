'''Техническое задание для проверки знаний программистов на FastAPI

Цель задания  
Создание простого API для управления списком задач (To-Do List) на FastAPI. Это позволит оценить знания кандидата в области разработки RESTful API, работы с базами данных и основами асинхронного программирования.

Требования  
1. Реализовать следующие конечные точки API:
   - Получить список всех задач (GET /tasks)
   - Получить задачу по ID (GET /tasks/{taskid})
   - Создать новую задачу (POST /tasks)
   - Обновить существующую задачу (PUT /tasks/{taskid})
   - Удалить задачу (DELETE /tasks/{taskid})

2. Формат данных:
   - Поля задачи:
     - id (integer, автоинкремент)
     - title (string)
     - description (string, опционально)
     - iscompleted (boolean, по умолчанию false)

3. Использовать SQLite в качестве базы данных.

4. Реализовать простую валидацию входящих данных.

5. Написать тесты для проверок функциональности API.'''
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
Base = declarative_base()
DATABASE_URL = "sqlite:///./todo.db"
engine = create_engine(DATABASE_URL)
sessionlocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key = True ,index = True)
    title = Column(String,index = True)
    description = Column(String,nullable = True,index = True)
    iscompleted = Column(Boolean, default = False)
Base.metadata.create_all(bind = engine)
app = FastAPI()
class TaskCreate(BaseModel):
   title: str
   description: Optional[str] = None
class TaskUpdate(BaseModel):
   title: Optional[str] = None
   description: Optional[str] = None
   iscompleted: Optional[bool] = None
@app.get('/tasks',response_model = List[TaskCreate])
def read_task(skip: int = 0, limit: int = 10):
    db: Session = sessionlocal()
    tasks = db.query(Task).offset(skip).limit(limit).all()
    return tasks
@app.get('/tasks/{task_id}',response_model = TaskCreate)
def read_task(task_id: int):
   db: Session = sessionlocal()
   task = db.query(Task).filter(Task.id == task_id).first()
   if task is None:
      raise HTTPException(status_code = 404,detail = 'Такой задачи нет')
   return task
@app.post('/tasks', response_model = TaskCreate)
def create_task(task: TaskCreate):
   db: Session = sessionlocal()
   db_task = Task(title = task.title, description = task.description)
   db.add(db_task)
   db.commit()
   db.refresh(db_task)
   return db_task
@app.put('/tasks/{task_id}', response_model = TaskCreate)
def update_task(task_id: int, task: TaskUpdate):
   db: Session = sessionlocal()
   db_task = db.query(Task).filter(Task.id == task_id).first()
   if db_task is None:
      raise HTTPException(status_code = 404,detail = "Такой задачи нет")
   if task.title is not None:
      db_task.title = task.title
   if task.description is not None:
      db_task.description = task.description
   if task.iscompleted is not None:
      db_task.iscompleted = task.iscompleted
   db.commit()
   db.refresh(db_task)
   return db_task
@app.delete('/tasks/{task_id}')
def delete_task(task_id: int):
   db: Session = sessionlocal()
   db_task = db.query(Task).filter(Task.id == task_id).first()
   if db_task is None:
      raise HTTPException(status_code = 404,detail = "Такой задачи нет")
   db.delete(db_task)
   db.commit()
   return {"detail": "Task deleted"}