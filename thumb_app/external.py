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
