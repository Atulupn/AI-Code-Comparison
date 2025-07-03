from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Создаем приложение
app = FastAPI()

# Модель задачи (теперь без обязательного id!)
class Task(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

# "База данных" в памяти
tasks_db = []
current_id = 1  # Счетчик для автоматического id

# Добавить задачу
@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    global current_id
    task_data = task.dict()
    task_data["id"] = current_id  # Автоматически добавляем id
    current_id += 1
    tasks_db.append(task_data)
    return task_data

# Получить все задачи
@app.get("/tasks/", response_model=List[dict])
def get_tasks():
    return tasks_db

# Получить одну задачу
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# Обновить задачу
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    for task in tasks_db:
        if task["id"] == task_id:
            task.update(updated_task.dict())
            task["id"] = task_id  # Сохраняем оригинальный id
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# Удалить задачу
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks_db
    tasks_db = [task for task in tasks_db if task["id"] != task_id]
    return {"message": "Task deleted"}
