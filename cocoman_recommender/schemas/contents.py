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
                     Column('contents_id', Integer, ForeignKey('TB_CONTENTS.id'), primary_key=True),
                     Column('ott_id', Integer, ForeignKey('TB_OTT.id'), primary_key=True)
                     )
contents_actor = Table('contents_actor', Base.metadata,
                       Column('contents_id', Integer, ForeignKey('TB_CONTENTS.id'), primary_key=True),
                       Column('actor_id', Integer, ForeignKey('TB_ACTOR.id'), primary_key=True)
                       )
contents_director = Table('contents_director', Base.metadata,
                          Column('contents_id', Integer, ForeignKey('TB_CONTENTS.id'), primary_key=True),
                          Column('director_id', Integer, ForeignKey('TB_DIRECTOR.id'), primary_key=True)
                          )
contents_genre = Table('contents_genre', Base.metadata,
                       Column('contents_id', Integer, ForeignKey('TB_CONTENTS.id'), primary_key=True),
                       Column('genre_id', Integer, ForeignKey('TB_GENRE.id'), primary_key=True)
                       )
contents_keyword = Table('contents_keyword', Base.metadata,
                         Column('contents_id', Integer, ForeignKey('TB_CONTENTS.id'), primary_key=True),
                         Column('keyword_id', Integer, ForeignKey('TB_KEYWORD.id'), primary_key=True)
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
    ott_id = relationship('Ott', secondary=contents_ott, lazy='dynamic')
    actors_id = relationship('Actor', secondary=contents_actor, back_populates='contents_set', lazy='dynamic')
    directors_id = relationship('Director', secondary=contents_director, back_populates='contents_set', lazy='dynamic')
    genres_id = relationship('Genre', secondary=contents_genre, back_populates='contents_set', lazy='dynamic')
    keywords_id = relationship('Keyword', secondary=contents_keyword, back_populates='contents_set', lazy='dynamic')


class ContentsRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(session_factory)

    def get_all(self) -> List[Contents]:
        with self.session_factory() as session:
            return session.query(Contents).all()

    def get_by_id(self, id: int):
        with self.session_factory() as session:
            return session.query(Contents).filter(Contents.id == id).one()

    def create(self, entity: Contents):
        with self.session_factory() as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity

    def delete_by_id(self, id: int):
        with self.session_factory() as session:
            session.query(Contents).filter(Contents.id == id).delete(synchronize_session='fetch')
            session.commit()

    def update(self, id: int, entity: Contents):
        with self.session_factory() as session:
            content = session.query(Contents).filter(Contents.id == id).one()
            content.title = entity.title
            content.year = entity.year
            content.country = entity.country
            content.running_time = entity.running_time
            content.grade_rate = entity.grade_rate
            content.broadcaster = entity.broadcaster
            content.open_date = entity.open_date
            content.broadcast_date = entity.broadcast_date
            content.story = entity.story
            content.poster_path = entity.poster_path
            content.ott_id = entity.ott_id
            content.actors_id = entity.actors_id
            content.directors_id = entity.directors_id
            content.genres_id = entity.genres_id
            content.keywords_id = entity.keywords_id
            session.commit()

            session.refresh(content)
            return content
