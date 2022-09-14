from enum import Enum
from io import BytesIO
from typing import Optional

import httpx
from fastapi import FastAPI
from PIL import Image
from pydantic import BaseModel
from starlette.config import Config

config = Config(".env")
ACCESS_KEY = config("ACCESS_KEY")
SEARCH_URL = "https://api.unsplash.com/search/photos"
app = FastAPI()


class OrientationEnum(str, Enum):
    portrait = "portrait"
    landscape = "landscape"
    squarish = "squarish"


class ColorEnum(str, Enum):
    black_and_white = "black_and_white"
    black = "black"
    white = "white"
    yellow = "yellow"
    orange = "orange"
    red = "red"
    purple = "purple"
    magenta = "magenta"
    green = "green"
    teal = "teal"
    blue = "blue"


class SearchModel(BaseModel):
    orientation: OrientationEnum
    color: ColorEnum


@app.get("/")
def hello():
    return {"hello": "world"}


def create_thumbnail(buffered_image: BytesIO):
    image = Image.open(buffered_image)
    return image.thumbnail(
        size=(200, image.height * 200 // image.width), resample=Image.Resampling.LANCZOS
    )


@app.get("/search/{query}")
async def search(
    query: str,
    orientation: Optional[OrientationEnum] = None,
    color: Optional[ColorEnum] = None,
):
    search_url = SEARCH_URL + f"?query={query}"
    if orientation is not None:
        search_url += f"&orientation={orientation.value}"
    if color is not None:
        search_url += f"&color={color.value}"
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
