from strawberry.fastapi import BaseContext
from databases import Database

class Context(BaseContext):
    def __init__(self, db: Database):
        self.db = db
