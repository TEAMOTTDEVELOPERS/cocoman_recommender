from sqlalchemy import (
    Column,
    Integer,
    String
)
from typing import List
from sqlalchemy.orm import relationship

from cocoman_recommender.schemas.base_repository import BaseRepository
from cocoman_recommender.schemas.contents import contents_actor
from cocoman_recommender.schemas.conn import Base


class Actor(Base):
    __tablename__ = 'TB_ACTOR'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255), nullable=False)
    image_path = Column(String(length=255))
    contents_set = relationship('Contents', secondary=contents_actor, back_populates='actors_id')


class ActorRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(session_factory)

    def get_all(self) -> List[Actor]:
        with self.session_factory() as session:
            return session.query(Actor).all()

    def get_by_id(self, id: int) -> Actor:
        with self.session_factory() as session:
            return session.query(Actor).filter(Actor.id == id).one()
