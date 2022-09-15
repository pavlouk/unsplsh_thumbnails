from re import L
from typing import Optional

from pydantic import BaseModel

from .enums import ColorEnum, OrientationEnum


class SearchBase(BaseModel):
    query: str
    color: Optional[ColorEnum] = None
    orientation: Optional[OrientationEnum] = None


class Image(SearchBase):
    is_active: bool
    clicks: int

    class Config:
        orm_mode = True


class ImageInfo(Image):
    url: str
    admin_url: str
