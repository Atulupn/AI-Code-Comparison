from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Создание приложения FastAPI
app = FastAPI()

# Класс модели задачи
class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    done: bool = False

# Временное хранилище задач (в памяти)
tasks: List[Task] = []

# Получить список всех задач
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

# Получить задачу по ID
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Задача не найдена")

# Создать новую задачу
@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    # Проверка: нет ли задачи с таким же ID
    for existing_task in tasks:
        if existing_task.id == task.id:
            raise HTTPException(status_code=400, detail="Задача с таким ID уже существует")
    tasks.append(task)
    return task

# Обновить существующую задачу
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Задача не найдена")

# Удалить задачу
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(index)
            return {"detail": "Задача удалена"}
    raise HTTPException(status_code=404, detail="Задача не найдена")
