from pydantic import BaseSettings, PostgresDsn, RedisDsn


class Settings(BaseSettings):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    database_dsn: PostgresDsn
    redis_dsn: RedisDsn

    bbb_server_name: str
    bbb_server_url: str
    bbb_secret_key: str
    bbb_attendee_pw: str
    bbb_mod_pw: str
