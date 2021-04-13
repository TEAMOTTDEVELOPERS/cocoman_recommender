from sqlalchemy import (
    Column,
    Integer,
    String
)
from typing import List
from sqlalchemy.orm import relationship

from cocoman_recommender.schemas.base_repository import BaseRepository
from cocoman_recommender.schemas.conn import Base


class User(Base):
    __tablename__ = 'TB_USER'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(length=255))
    social_id = Column(String(length=255))
    nick_name = Column(String(length=100), nullable=False, unique=True)
    password = Column(String(length=100))
    age = Column(Integer, nullable=False)
    gender = Column(String(length=255), nullable=False)
    phone_number = Column(String(length=255))
    profile_img = Column(String(length=255))
    push_token = Column(String(length=255))
    review_set = relationship('Review', back_populates='user')


class UserRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(session_factory)

    def get_all(self) -> List[User]:
        with self.session_factory() as session:
            return session.query(User).all()
