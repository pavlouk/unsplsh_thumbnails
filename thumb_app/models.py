from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.sqlite import BLOB

from .database import Base


class Thumbnail(Base):
    __tablename__ = "thumbnails"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    secret_key = Column(String, unique=True, index=True)
    thumbnail_image = Column(BLOB, index=True)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)
