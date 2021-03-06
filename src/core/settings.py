import os


def _get_database_url() -> str:
    try:
        url = 'postgresql://'
        url += POSTGRES_USER + ':'
        url += POSTGRES_PASSWORD + '@'
        url += POSTGRES_HOST + ':'
        url += POSTGRES_PORT + '/'
        url += POSTGRES_DB
        return url
    except TypeError as ex:
        raise TypeError(
            'Some settings not added to .envfile! \n' + str(ex)
        )


SECRET_KEY: str = os.environ.get('SECRET_KEY')
ALGORITHM: str = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080

POSTGRES_HOST: str = os.environ.get('POSTGRES_HOST')
POSTGRES_USER: str = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD: str = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_DB: str = os.environ.get('POSTGRES_DB')
POSTGRES_PORT: str = os.environ.get('POSTGRES_PORT')
DATABASE_URL: str = os.environ.get('DATABASE_URL') or _get_database_url()

BBB_SERVER_NAME: str = os.environ.get('BBB_SERVER_NAME')
BBB_SERVER_URL: str = os.environ.get('BBB_SERVER_URL')
BBB_SECRET_KEY: str = os.environ.get('BBB_SECRET_KEY')
BBB_ATTENDEE_PW: str = os.environ.get('BBB_ATTENDEE_PW')
BBB_MOD_PW: str = os.environ.get('BBB_MOD_PW')

REDIS_HOST: str = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT: str = str(os.environ.get('REDIS_PORT', 6379))
REDIS_PASSWORD: str = os.environ.get('REDIS_PASSWORD', '')
REDIS_DB: int = int(os.environ.get('REDIS_DB', 0))
REDIS_URL: str = os.environ.get('REDIS_URL', 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/' + str(REDIS_DB))  # noqa: E501
