from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator

# for loading environment variable from .env file into our project
# standard practice
# allows us to take all the env variable and map them to python object, so that we can use and reference it
# throughout the code
# BaseSetting - class
# pydantic - library it allows us to handle advance python data handling and map data that is not python obj
# into python obj
# ENVIRONMENT variable mentioned in Setting class should match with .env variable name
# @field validator - to convert allowed string data from comma seperated string to LIST

class Settings(BaseSettings):  # inheriting from class 'BaseSettings'
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = True

    DATABASE_URL: str
    ALLOWED_ORIGINS: str = ""

    OPENAI_API_KEY: str

    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v: str) -> List[str]:
        return v.split(",") if v else []

    class Config:  # making sure that python loads the environment correctly from the correct file
        env_file = ".env"  # env variable file name
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()





