import os
from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

"""
# 윈도우
set APP_ENV=dev
uvicorn main:app

# 리눅스
export APP_ENV=dev
uvicorn main:app
"""


class Settings(BaseSettings):
    APP_ENV: str = "local"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        database = {
            "MODE": "Settings",
            "HOST": "192.168.1.131",
            "PORT": "5432",
            "NAME": "test",
            "USER": "dev",
            "PASSWORD": "dev1234",
            "POOL-MIN": 1,
            "POOL-MAX": 10
        }  # fmt: skip


class DevSettings(Settings):
    class Config:
        env_file = "dev.env"
        database = {
            "MODE": "DevSettings",
            "HOST": "192.168.1.131",
            "PORT": "5432",
            "NAME": "test",
            "USER": "dev",
            "PASSWORD": "dev1234",
            "POOL-MIN": 1,
            "POOL-MAX": 10
        }  # fmt: skip


class ProdSettings(Settings):
    class Config:
        env_file = "prod.env"
        database = {
            "MODE": "ProdSettings",
            "HOST": "112.217.168.242",
            "PORT": "5432",
            "NAME": "test",
            "USER": "maxted",
            "PASSWORD": "maxted1234",
            "POOL-MIN": 5,
            "POOL-MAX": 100
        }  # fmt: skip


class FactorySettings:
    @staticmethod
    def load():
        app_env = Settings().APP_ENV
        if app_env == "dev":
            settings = DevSettings()
            return settings
        elif app_env == "prod":
            settings = ProdSettings()
            return settings
        else:
            settings = Settings()

        print("## Settings.APP_ENV:", app_env)
        return settings


settings = FactorySettings.load()
load_dotenv(settings.Config.env_file)
