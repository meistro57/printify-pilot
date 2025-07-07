"""Asset Storage Agent.
Stores uploaded design assets to a local directory as a placeholder for cloud storage."""

from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

UPLOAD_DIR = Path(__file__).resolve().parents[1] / 'uploads'
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def upload_asset(file: UploadFile) -> str:
    """Save an uploaded file and return its path."""
    extension = Path(file.filename).suffix
    dest = UPLOAD_DIR / f"{uuid4().hex}{extension}"
    with dest.open('wb') as out:
        out.write(file.file.read())
    return str(dest)
