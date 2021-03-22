from os import path, environ
from dataclasses import dataclass

BASE_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))


@dataclass
class Config:
    BASE_DIR: str = BASE_DIR
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True
    DEBUG: bool = False
    TEST_MODE: bool = False
    DB_URL: str = environ.get("DB_URL", "")


@dataclass
class LocalConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    DEBUG: bool = True


@dataclass
class ProdConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]


@dataclass
class TestConfig:
    DB_URL: str = "mysql+pymysql://travis@localhost/notification_test?charset=utf8mb4"
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    TEST_MODE: bool = True


def conf():
    config = dict(prod=ProdConfig, local=LocalConfig, test=TestConfig)
    return config[environ.get("API_ENV", "local")]()
