import databases
import sqlalchemy

from core.settings import Settings

settings = Settings()

database = databases.Database(settings.DATABASE_URL)
metadata = sqlalchemy.MetaData()
