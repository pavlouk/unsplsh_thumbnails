from typing import Optional

from pydantic import BaseModel

from .enums import ColorEnum, OrientationEnum


class SearchBase(BaseModel):
    query: str
    color: Optional[ColorEnum] = None
    orientation: Optional[OrientationEnum] = None
