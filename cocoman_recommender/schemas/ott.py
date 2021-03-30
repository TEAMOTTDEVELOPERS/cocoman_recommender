from sqlalchemy import (
    Column,
    Integer,
    String
)
from typing import List

from cocoman_recommender.schemas.base_repository import BaseRepository
from cocoman_recommender.schemas.conn import Base


class Ott(Base):
    __tablename__ = 'TB_OTT'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255))
    image_path = Column(String(length=255))


class OttRepository(BaseRepository):
    def get_all(self) -> List[Ott]:
        return self.session.query(Ott).all()
