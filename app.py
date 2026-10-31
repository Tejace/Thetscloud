from fastapi import FastAPI
from src.utils.db import Base, engine
from src.tasks.models import TaskModel
from src.user.models import UserModel
from src.files.models import FileModel
from src.tasks.router import task_routes
from src.user.router import user_routes
from src.files.routes import file_routes
from fastapi.staticfiles import StaticFiles
from pathlib import Path

Base.metadata.create_all(engine)


app = FastAPI(title="task manager appp")
app.include_router(task_routes)
app.include_router(user_routes)
app.include_router(file_routes)
app.mount("/", StaticFiles(directory=Path(__file__).parent / "static", html=True), name="static")