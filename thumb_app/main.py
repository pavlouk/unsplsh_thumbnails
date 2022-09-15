import secrets
from io import BytesIO

import validators
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from . import models, schemas
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


# , response_model=schemas.ImageInfo
@app.post("/search")
async def image_search(search: schemas.SearchBase, db: Session = Depends(get_db)):
    if not validators.url(unsplash_builder(search)):  # type: ignore
        raise_bad_request(message="Your provided query is not valid")
    thumbnail_string = await fetch_image(unsplash_builder(search))
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = "".join(secrets.choice(chars) for _ in range(5))
    secret_key = "".join(secrets.choice(chars) for _ in range(8))
    # return Response(thumbnail_string, media_type="image/jpeg")  # type: ignore
    db_thumbnail = models.Thumbnail(
        thumbnail_image=thumbnail_string, key=key, secret_key=secret_key
    )
    db.add(db_thumbnail)
    db.commit()
    db.refresh(db_thumbnail)
    db_thumbnail.url = key
    db_thumbnail.admin_url = secret_key

    return f"TODO: Create database entry for: thumbnail_string"  # type: ignore
