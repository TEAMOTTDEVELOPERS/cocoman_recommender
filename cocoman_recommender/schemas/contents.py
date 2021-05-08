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
from cocoman_recommender.schemas.ott import Ott

contents_ott = Table('contents_ott', Base.metadata,
                     Column('contents_id', Integer, ForeignKey('TB_CONTENTS.id'), primary_key=True),
                     Column('ott_id', Integer, ForeignKey('TB_OTT.id'), primary_key=True)
                     )
contents_actor = Table('contents_actor', Base.metadata,
                       Column('contents_id', Integer, ForeignKey('TB_CONTENTS.id'), primary_key=True),
                       Column('actors_id', Integer, ForeignKey('TB_ACTOR.id'), primary_key=True)
                       )
contents_director = Table('contents_director', Base.metadata,
                          Column('contents_id', Integer, ForeignKey('TB_CONTENTS.id'), primary_key=True),
                          Column('directors_id', Integer, ForeignKey('TB_DIRECTOR.id'), primary_key=True)
                          )
contents_genre = Table('contents_genre', Base.metadata,
                       Column('contents_id', Integer, ForeignKey('TB_CONTENTS.id'), primary_key=True),
                       Column('genres_id', Integer, ForeignKey('TB_GENRE.id'), primary_key=True)
                       )
contents_keyword = Table('contents_keyword', Base.metadata,
                         Column('contents_id', Integer, ForeignKey('TB_CONTENTS.id'), primary_key=True),
                         Column('keywords_id', Integer, ForeignKey('TB_KEYWORD.id'), primary_key=True)
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
    ott = relationship('Ott', secondary=contents_ott, lazy='dynamic')
    actors = relationship('Actor', secondary=contents_actor, back_populates='contents_set', lazy='dynamic')
    directors = relationship('Director', secondary=contents_director, back_populates='contents_set', lazy='dynamic')
    genres = relationship('Genre', secondary=contents_genre, back_populates='contents_set', lazy='dynamic')
    keywords = relationship('Keyword', secondary=contents_keyword, back_populates='contents_set', lazy='dynamic')


class ContentsRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(session_factory)

    def get_all(self) -> List[Contents]:
        with self.session_factory() as session:
            return session.query(Contents).all()

    def get_all_by_ott(self, name) -> List[Contents]:
        with self.session_factory() as session:
            return session.query(Contents).join(Contents.ott).filter(Ott.name == name).all()

    def get_by_id(self, id: int):
        with self.session_factory() as session:
            return session.query(Contents).filter(Contents.id == id).one()

    def get_by_title(self, title: str):
        with self.session_factory() as session:
            return session.query(Contents).filter(Contents.title == title).one()

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
            content.ott = entity.ott
            content.actors = entity.actors
            content.directors = entity.directors
            content.genres = entity.genres
            content.keywords = entity.keywords
            session.commit()

            session.refresh(content)
            return content
