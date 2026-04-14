import os
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings


ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}


def validate_file_type(filename: str) -> None:
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file type. Upload PDF, JPG, JPEG, or PNG")


def ensure_upload_dir() -> Path:
    path = Path(settings.upload_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


async def save_upload_file(upload: UploadFile) -> tuple[str, str]:
    validate_file_type(upload.filename or "")
    upload_dir = ensure_upload_dir()
    ext = Path(upload.filename or "").suffix.lower()
    unique_name = f"{uuid4().hex}{ext}"
    target = upload_dir / unique_name

    content = await upload.read()
    max_size = settings.max_upload_mb * 1024 * 1024
    if len(content) > max_size:
        raise ValueError(f"File too large. Max allowed size is {settings.max_upload_mb} MB")

    with open(target, "wb") as f:
        f.write(content)
    return unique_name, os.fspath(target)
