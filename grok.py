from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn

# Создаем экземпляр FastAPI приложения
app = FastAPI(title="To-Do List API")

# Модель для задачи (определяет, какие данные должна содержать задача)
class Task(BaseModel):
    id: int
    title: str
    description: str | None = None  # Описание необязательное
    completed: bool = False  # По умолчанию задача не выполнена

# Хранилище задач в памяти (список словарей)
tasks: List[Task] = []

# Эндпоинт для создания новой задачи
@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    # Проверяем, не существует ли уже задача с таким ID
    for existing_task in tasks:
        if existing_task.id == task.id:
            raise HTTPException(status_code=400, detail="Task with this ID already exists")
    tasks.append(task)
    return task

# Эндпоинт для получения всех задач
@app.get("/tasks/", response_model=List[Task])
def get_tasks():
    return tasks

# Эндпоинт для получения задачи по ID
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# Эндпоинт для обновления задачи
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            if task_id != updated_task.id:
                raise HTTPException(status_code=400, detail="Cannot change task ID")
            tasks[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

# Эндпоинт для удаления задачи
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(index)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")

# Запуск сервера
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)