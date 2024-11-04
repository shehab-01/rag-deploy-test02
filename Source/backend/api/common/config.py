from dataclasses import dataclass
from os import path, environ
from typing import List

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))


# 기본 Configuration
@dataclass
class Config:
    DEBUG: bool = False
    TEST_MODE: bool = False
    BASE_DIR: str = base_dir
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True
    DB_URL: str = environ.get("DB_URL", "")


@dataclass
class LocalConfig(Config):
    DEBUG: bool = True
    ALLOW_SITE = ["*"]
    TRUSTED_HOSTS = ["*"]


@dataclass
class ProdConfig(Config):
    ALLOW_SITE = ["*"]
    TRUSTED_HOSTS = ["*"]


@dataclass
class TestConfig(Config):
    TEST_MODE: bool = True
    ALLOW_SITE = ["*"]
    TRUSTED_HOSTS = ["*"]
    DB_URL: str = ""


# 환경 불러오기
def conf():
    config = dict(prod=ProdConfig, local=LocalConfig, test=TestConfig)
    return config[environ.get("APP_ENV", "local")]()
