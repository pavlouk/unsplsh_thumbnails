import validators
from fastapi import FastAPI, HTTPException

from . import schemas
from .external import unsplash_builder

app = FastAPI()


@app.get("/")
def read_root():
    return "Welcome to the unofficial Unsplash thumbnails API!"


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


@app.post("/search")
def image_search(search: schemas.SearchBase):
    if not validators.url(unsplash_builder(search)):  # type: ignore
        raise_bad_request(message="Your provided query is not valid")
    return f"TODO: Create database entry for: {search.query}"
