from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)
from typing import List
from sqlalchemy.orm import relationship, backref

from cocoman_recommender.schemas.base_repository import BaseRepository
from cocoman_recommender.schemas.conn import Base


class SearchHistory(Base):
    __tablename__ = 'TB_SEARCH_HISTORY'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('TB_USER.id'))
    user = relationship('User', backref=backref('search_histories'))
    contents_id = Column(Integer, ForeignKey('TB_CONTENTS.id'))
    contents = relationship('Contents', backref=backref('search_histories'))
    search_keyword = Column(String(length=255))


class SearchHistoryRepository(BaseRepository):
    def get_all(self) -> List[SearchHistory]:
        return self.session.query(SearchHistory).all()
