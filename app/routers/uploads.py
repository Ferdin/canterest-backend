import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import aiofiles

from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/uploads", tags=["uploads"])

UPLOAD_DIR = "app/static/uploads"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".mp4", ".mov"}
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

@router.post("/media")
async def upload_media(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    ext = os.path.splitext(file.filename)[1].lower()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(400, "File too large (max 20MB)")

    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    async with aiofiles.open(filepath, "wb") as f:
        await f.write(contents)

    media_url = f"http://localhost:8000/static/uploads/{filename}"
    return {"media_url": media_url}      