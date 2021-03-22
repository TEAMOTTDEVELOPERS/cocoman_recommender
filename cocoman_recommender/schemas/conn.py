from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import close_all_sessions
import logging


def _database_exist(engine, schema_name):
    query = f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{schema_name}'"
    with engine.connect() as conn:
        result_proxy = conn.execute(query)
        result = result_proxy.scalar()
        return bool(result)


def _drop_database(engine, schema_name):
    with engine.connect() as conn:
        conn.execute(f"DROP DATABASE {schema_name};")


def _create_database(engine, schema_name):
    with engine.connect() as conn:
        conn.execute(f"CREATE DATABASE {schema_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;")


class SQLAlchemy:
    def __init__(self, app: FastAPI = None, **kwargs):
        self._engine = None
        self._session = None
        if app is not None:
            self.init_app(app=app, **kwargs)

    def init_app(self, app: FastAPI, **kwargs):
        database_url = kwargs.get("DB_URL")
        pool_recycle = kwargs.setdefault("DB_POOL_RECYCLE", 900)
        is_testing = kwargs.setdefault("TEST_MODE", False)
        echo = kwargs.setdefault("DB_ECHO", True)

        self._engine = create_engine(
            database_url,
            echo=echo,
            pool_recycle=pool_recycle,
            pool_pre_ping=True,
        )
        if is_testing:
            db_url = self._engine.url
            if db_url.host != "localhost":
                raise Exception("DB host must be 'localhost' in test environment")
            except_schema_db_url = f"{db_url.drivername}://{db_url.username}@{db_url.host}"
            schema_name = db_url.database
            temp_engine = create_engine(except_schema_db_url, echo=echo, pool_recycle=pool_recycle, pool_pre_ping=True)
            if _database_exist(temp_engine, schema_name):
                _drop_database(temp_engine, schema_name)
            _create_database(temp_engine, schema_name)
            temp_engine.dispose()

        self._session = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

        @app.on_event("startup")
        def startup():
            self._engine.connect()
            logging.info("DB connected.")

        @app.on_event("shutdown")
        def shutdown():
            close_all_sessions()
            self._engine.dispose()
            logging.info("DB disconnected.")

    def get_db(self):
        if self._session is None:
            raise Exception("Must be called 'init_app'")
        db_session = None
        try:
            db_session = self._session()
            yield db_session
        finally:
            db_session.close()

    @property
    def session(self):
        return self.get_db

    @property
    def engine(self):
        return self._engine


db = SQLAlchemy()
Base = declarative_base()
