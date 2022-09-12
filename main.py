from typing import Optional

import httpx
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
async def search(
    query: str, orientation: Optional[str] = None, color: Optional[str] = None
):
    search_url = SEARCH_URL + f"?query={query}"
    if orientation is not None:
        search_url += f"&orientation={orientation}"
    if color is not None:
        search_url += f"&color={color}"
    search_url += f"&client_id={ACCESS_KEY}"
    async with httpx.AsyncClient() as client:
        resp = httpx.get(search_url)
        resp.raise_for_status()
        data = resp.json()
    return {search_url: data}
