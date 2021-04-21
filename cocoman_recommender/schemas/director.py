from sqlalchemy import (
    Column,
    Integer,
    String
)
from typing import List
from sqlalchemy.orm import relationship

from cocoman_recommender.schemas.base_repository import BaseRepository
from cocoman_recommender.schemas.contents import contents_director
from cocoman_recommender.schemas.conn import Base


class Director(Base):
    __tablename__ = 'TB_DIRECTOR'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255), nullable=False)
    image_path = Column(String(length=255))
    contents_set = relationship('Contents', secondary=contents_director, back_populates='directors_id')


class DirectorRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(session_factory)

    def get_all(self) -> List[Director]:
        with self.session_factory() as session:
            return session.query(Director).all()

    def get_by_id(self, id: int) -> Director:
        with self.session_factory() as session:
            return session.query(Director).filter(Director.id == id).one()
