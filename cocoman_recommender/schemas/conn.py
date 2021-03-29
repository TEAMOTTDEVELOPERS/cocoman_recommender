from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, Session
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()


class SQLAlchemy:
    def __init__(self, url: str):
        self._engine = create_engine(url, echo=True)
        self._session = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def create_database(self):
        Base.metadata.create_all(self._engine)

    @property
    def session(self):
        session: Session = self._session
        try:
            yield session
        except Exception:
            logger.exception('Session rollback because of exception')
            session.rollback()
            raise
        finally:
            session.close()
