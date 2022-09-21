import secrets

import validators
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session

from . import models, schemas
from .config import get_settings
from .database import SessionLocal, engine
from .external import fetch_image, unsplash_builder

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return "Welcome to the unofficial Unsplash thumbnails API!"


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


@app.post("/search")
async def image_search(search: schemas.SearchBase, db: Session = Depends(get_db)):
    if not validators.url(unsplash_builder(search)):  # type: ignore
        raise_bad_request(message="Your provided query is not valid")
    thumbnail_string = await fetch_image(unsplash_builder(search))
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = "".join(secrets.choice(chars) for _ in range(5))
    db_thumbnail = models.Thumbnail(thumbnail_image=thumbnail_string, key=key)
    db.add(db_thumbnail)
    db.commit()
    db.refresh(db_thumbnail)

    return {"Access your thumbnail at: ": f"{get_settings().base_url}/{key}"}  # type: ignore


def raise_not_found(request):
    message = f"Thumbnail with URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)


@app.get("/{thumbnail_key}")
def show_thumbnail(thumbnail_key: str, request: Request, db: Session = Depends(get_db)):
    db_thumbnails = db.query(models.Thumbnail).filter(models.Thumbnail.key == thumbnail_key).first()  # type: ignore
    if db_thumbnails:
        return Response(db_thumbnails.thumbnail_image, media_type="image/jpeg")  # type: ignore
    else:
        raise_not_found(request)
