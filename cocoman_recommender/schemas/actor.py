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
    def get_all(self) -> List[Actor]:
        return self.session.query(Actor).all()
