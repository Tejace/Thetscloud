from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from src.files import controller
from src.utils.db import get_db
from src.utils.helpers import is_auth
from src.user.models import UserModel


file_routes = APIRouter(prefix="/files", tags=["Files"])


@file_routes.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_auth),
):
    return await controller.upload_file(file, db, user)


@file_routes.get("/")
def get_my_files(
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_auth),
):
    return controller.get_my_files(db, user)


@file_routes.get("/download/{file_id}")
def download_file(
    file_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_auth),
) -> FileResponse:
    return controller.download_file(file_id, db, user)


@file_routes.delete(
    "/{file_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_file(
    file_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_auth),
):
    controller.delete_file(file_id, db, user)