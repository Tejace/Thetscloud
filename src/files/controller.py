from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from src.files.models import FileModel
from src.user.models import UserModel
from src.utils.settings import settings


UPLOAD_DIR = Path(settings.UPLOAD_DIR).expanduser().resolve()
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB


async def upload_file(
    file: UploadFile,
    db: Session,
    user: UserModel,
):
    original_filename = Path(file.filename or "").name

    if not original_filename or original_filename in {".", ".."}:
        raise HTTPException(
            status_code=400,
            detail="Invalid filename",
        )

    extension = Path(original_filename).suffix.lower()
    stored_filename = f"{uuid4().hex}{extension}"
    file_path = UPLOAD_DIR / stored_filename

    size = 0
    record = None

    try:
        with file_path.open("xb") as buffer:
            while True:
                chunk = await file.read(1024 * 1024)

                if not chunk:
                    break

                size += len(chunk)

                if size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="File exceeds the 20 MB limit",
                    )

                buffer.write(chunk)

        record = FileModel(
            original_filename=original_filename,
            stored_filename=stored_filename,
            content_type=file.content_type,
            size=size,
            user_id=user.id,
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return {
            "message": "File uploaded successfully",
            "data": {
                "id": record.id,
                "filename": record.original_filename,
                "content_type": record.content_type,
                "size": record.size,
                "created_at": record.created_at,
            },
        }

    except Exception:
        db.rollback()
        file_path.unlink(missing_ok=True)
        raise

    finally:
        await file.close()


def get_my_files(
    db: Session,
    user: UserModel,
):
    files = (
        db.query(FileModel)
        .filter(FileModel.user_id == user.id)
        .all()
    )

    return {
        "message": "Your files retrieved successfully",
        "data": [
            {
                "id": item.id,
                "filename": item.original_filename,
                "content_type": item.content_type,
                "size": item.size,
                "created_at": item.created_at,
            }
            for item in files
        ],
    }


def download_file(
    file_id: int,
    db: Session,
    user: UserModel,
):
    record = (
        db.query(FileModel)
        .filter(
            FileModel.id == file_id,
            FileModel.user_id == user.id,
        )
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="File not found",
        )

    file_path = UPLOAD_DIR / record.stored_filename

    if not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="File data not found on storage",
        )

    return FileResponse(
        path=file_path,
        filename=record.original_filename,
        media_type="application/octet-stream",
    )


def delete_file(
    file_id: int,
    db: Session,
    user: UserModel,
):
    record = (
        db.query(FileModel)
        .filter(
            FileModel.id == file_id,
            FileModel.user_id == user.id,
        )
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="File not found",
        )

    file_path = UPLOAD_DIR / record.stored_filename

    try:
        db.delete(record)
        db.commit()
    except Exception:
        db.rollback()
        raise

    file_path.unlink(missing_ok=True)

    return None