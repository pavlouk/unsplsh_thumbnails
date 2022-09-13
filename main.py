from io import BytesIO
from typing import Optional

import httpx
from fastapi import FastAPI
from PIL import Image
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
        response = httpx.get(search_url)
        response.raise_for_status()
        response_body = response.json()
        search_results = response_body.get("results", {})
        urls = search_results[0].get("urls", {})
        image_width = search_results[0].get("width", {})
        image_height = search_results[0].get("height", {})
        raw_url = urls.get("small", "Error")
        image_response = httpx.get(raw_url)
        image_buffer = BytesIO(image_response.content)
    return {
        "raw width": image_width,
        "raw height": image_height,
    }
