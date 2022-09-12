from typing import Optional

from fastapi import FastAPI
from starlette.config import Config

config = Config(".env")
ACCESS_KEY = config("ACCESS_KEY")
SEARCH_URL = "https://api.unsplash.com/search/photos"
app = FastAPI()


@app.get("/")
def hello():
    return {"hello": "world"}


@app.get("/search/{query}")
def search(query: str, orientation: Optional[str] = None, color: Optional[str] = None):
    search_url = SEARCH_URL + f"?query={query}"
    if orientation is not None:
        search_url += f"&orientation={orientation}"
    if color is not None:
        search_url += f"&color={color}"
    search_url += ACCESS_KEY
    return {"Search using": search_url}
