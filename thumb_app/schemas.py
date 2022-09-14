from pydantic import BaseModel


class SearchBase(BaseModel):
    query: str
    color: str
    orientation: str
