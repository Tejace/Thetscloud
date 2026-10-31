from fastapi import APIRouter, Depends, status
from src.tasks import controller
from src.tasks.dtos import TaskSchema
from src.utils.db import get_db
from src.utils.helpers import is_auth
from src.user.models import UserModel

task_routes = APIRouter(prefix="/tasks")

@task_routes.post("/create", status_code=status.HTTP_201_CREATED)
def create_task(body:TaskSchema, db = Depends(get_db), user:UserModel = Depends(is_auth)):
    return controller.create_task(body, db, user)


@task_routes.get("/get", status_code=status.HTTP_200_OK)
def get_all_tasks(db = Depends(get_db), user:UserModel = Depends(is_auth)):
    return controller.get_tasks(db, user)


@task_routes.get("/get_tasks_by_title/{task_title}", status_code=status.HTTP_200_OK)
def get_single_task(task_title:str ,db = Depends(get_db), user:UserModel = Depends(is_auth)):
    return controller.get_single_task(task_title, db, user)


@task_routes.put("/update_single/{task_id}", status_code=status.HTTP_201_CREATED)
def update_single_task(body:TaskSchema, task_id:int, db = Depends(get_db), user:UserModel = Depends(is_auth)):
    return controller.update_task(body, task_id, db, user)


@task_routes.delete("/delete_single/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_single_task(task_id:int, db = Depends(get_db), user:UserModel = Depends(is_auth)):
    return controller.delete_single_task(task_id, db, user)