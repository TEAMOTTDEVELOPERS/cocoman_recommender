from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey
)
from typing import List

from cocoman_recommender.schemas.base_repository import BaseRepository
from cocoman_recommender.schemas.conn import Base


class StarRating(Base):
    __tablename__ = 'TB_STAR'
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Float)
    user_id = Column(Integer, ForeignKey('TB_USER.id'))
    contents_id = Column(Integer, ForeignKey('TB_CONTENTS.id'))


class StarRatingRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(session_factory)

    def get_all(self) -> List[StarRating]:
        with self.session_factory() as session:
            return session.query(StarRating).all()
