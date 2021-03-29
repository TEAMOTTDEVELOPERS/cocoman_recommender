from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table
)
from typing import List
from sqlalchemy.orm import relationship

from cocoman_recommender.schemas.base_repository import BaseRepository
from cocoman_recommender.schemas.conn import Base

contents_ott = Table('contents_ott', Base.metadata,
                     Column('contents_id', Integer, ForeignKey('TB_CONTENTS.id')),
                     Column('ott_id', Integer, ForeignKey('TB_OTT.id'))
                     )
contents_actor = Table('contents_actor', Base.metadata,
                       Column('contents_id', Integer, ForeignKey('TB_CONTENTS.id')),
                       Column('actor_id', Integer, ForeignKey('TB_ACTOR.id'))
                       )
contents_director = Table('contents_director', Base.metadata,
                          Column('contents_id', Integer, ForeignKey('TB_CONTENTS.id')),
                          Column('director_id', Integer, ForeignKey('TB_DIRECTOR.id'))
                          )
contents_genre = Table('contents_genre', Base.metadata,
                       Column('contents_id', Integer, ForeignKey('TB_CONTENTS.id')),
                       Column('genre_id', Integer, ForeignKey('TB_GENRE.id'))
                       )
contents_keyword = Table('contents_keyword', Base.metadata,
                         Column('contents_id', Integer, ForeignKey('TB_CONTENTS.id')),
                         Column('keyword_id', Integer, ForeignKey('TB_KEYWORD.id'))
                         )


class Contents(Base):
    __tablename__ = 'TB_CONTENTS'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=255), nullable=False)
    year = Column(String(length=255), nullable=False)
    country = Column(String(length=255))
    running_time = Column(Integer)
    grade_rate = Column(String(length=255), nullable=False)
    broadcaster = Column(String(length=255))
    open_date = Column(String(length=255))
    broadcast_date = Column(String(length=255))
    story = Column(String(length=500), nullable=False)
    poster_path = Column(String(length=255))
    ott_id = relationship('Ott', secondary=contents_ott)
    actors_id = relationship('Actor', secondary=contents_actor, back_populates='contents_set')
    directors_id = relationship('Director', secondary=contents_director, back_populates='contents_set')
    genres_id = relationship('Genre', secondary=contents_genre, back_populates='contents_set')
    keywords_id = relationship('Keyword', secondary=contents_keyword, back_populates='contents_set')


class ContentsRepository(BaseRepository):
    def get_all(self) -> List[Contents]:
        return self.session.query(Contents).all()
