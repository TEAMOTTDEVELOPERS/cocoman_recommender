from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)
from typing import List
from sqlalchemy.orm import relationship

from cocoman_recommender.schemas.base_repository import BaseRepository
from cocoman_recommender.schemas.conn import Base


class Review(Base):
    __tablename__ = 'TB_REVIEW'
    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String(length=500))
    user_id = Column(Integer, ForeignKey('TB_USER.id'))
    user = relationship('User', back_populates='review_set')
    content_id = Column(Integer, ForeignKey('TB_CONTENTS.id'))
    contents_set = relationship('Contents')


class ReviewRepository(BaseRepository):
    def get_all(self) -> List[Review]:
        return self.session.query(Review).all()
