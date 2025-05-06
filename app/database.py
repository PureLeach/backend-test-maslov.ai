from databases import Database
from app.settings import settings


db = Database(settings.DATABASE_DSN)
