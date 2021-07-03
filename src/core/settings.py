import os

from dotenv import load_dotenv, find_dotenv

from pydantic import BaseSettings


load_dotenv(find_dotenv(filename='.envfile'))


class PostgresSettings:
    __postgres_host: str = os.environ.get('POSTGRES_HOST')
    __postgres_user: str = os.environ.get('POSTGRES_USER')
    __postgres_password: str = os.environ.get('POSTGRES_PASSWORD')
    __postgres_db: str = os.environ.get('POSTGRES_PASSWORD')
    __postgres_port: str = os.environ.get('POSTGRES_PORT')

    @classmethod
    def DATABASE_URL(cls) -> str:
        try:
            url = 'postgresql://'
            url += cls.__postgres_user + ':'
            url += cls.__postgres_password + '@'
            url += cls.__postgres_host + ':'
            url += cls.__postgres_port + '/'
            url += cls.__postgres_db
            return url
        except TypeError as ex:
            raise TypeError(
                'Some settings not added to .envfile! \n' + str(ex)
            )


class Settings(BaseSettings):
    SECRET_KEY: str = os.environ.get('SECRET_KEY')
    DATABASE_URL: str = PostgresSettings.DATABASE_URL()
