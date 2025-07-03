from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Создаем экземпляр FastAPI приложения
app = FastAPI()

# Класс для описания структуры задачи (модель данных)
class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None  # Описание необязательное
    completed: bool = False  # По умолчанию задача не выполнена

# "База данных" в памяти - просто список задач
tasks_db = []
current_id = 1  # Счетчик для генерации уникальных ID

# Маршрут для создания новой задачи
@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    """
    Создает новую задачу.
    Принимает JSON с title и description (опционально).
    Возвращает созданную задачу.
    """
    global current_id
    # Генерируем ID для новой задачи
    task.id = current_id
    current_id += 1
    # Добавляем задачу в "базу данных"
    tasks_db.append(task)
    return task

# Маршрут для получения списка всех задач
@app.get("/tasks/", response_model=List[Task])
def read_tasks():
    """
    Возвращает список всех задач.
    """
    return tasks_db

# Маршрут для получения одной задачи по ID
@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    """
    Возвращает задачу по указанному ID.
    Если задача не найдена, возвращает ошибку 404.
    """
    for task in tasks_db:
        if task.id == task_id:
            return task
    # Если задача не найдена, вызываем ошибку
    raise HTTPException(status_code=404, detail="Task not found")

# Маршрут для обновления задачи
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    """
    Обновляет существующую задачу.
    Принимает ID задачи и новые данные в формате JSON.
    Возвращает обновленную задачу.
    """
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            # Обновляем данные задачи
            updated_task.id = task_id
            tasks_db[i] = updated_task
            return updated_task
    # Если задача не найдена, вызываем ошибку
    raise HTTPException(status_code=404, detail="Task not found")

# Маршрут для удаления задачи
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """
    Удаляет задачу по указанному ID.
    Возвращает сообщение об успешном удалении.
    """
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            # Удаляем задачу из списка
            del tasks_db[i]
            return {"message": "Task deleted successfully"}
    # Если задача не найдена, вызываем ошибку
    raise HTTPException(status_code=404, detail="Task not found")