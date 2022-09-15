from io import BytesIO

import httpx
from PIL import Image

from . import schemas
from .config import get_settings


def unsplash_builder(search: schemas.SearchBase) -> str:
    search_url = get_settings().usplash_api + f"?query={search.query}"
    if search.orientation is not None:
        search_url += f"&orientation={search.orientation.value}"
    if search.color is not None:
        search_url += f"&color={search.color.value}"
    search_url += f"&client_id={get_settings().unsplash_key}"
    return search_url


def create_thumbnail(buffered_image: BytesIO):
    image = Image.open(buffered_image)
    return image.thumbnail(
        size=(200, image.height * 200 // image.width), resample=Image.Resampling.LANCZOS
    )


async def fetch_image(search_url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(search_url)
        response.raise_for_status()
        response_body = response.json()
        search_results = response_body.get("results", {})
        urls = search_results[0].get("urls", {})
        raw_url = urls.get("small", "Error")
        image_response = await client.get(raw_url)
        response.raise_for_status()
        image_buffer = BytesIO(image_response.content)
        return create_thumbnail(image_buffer)
