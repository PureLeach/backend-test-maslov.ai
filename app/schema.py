from contextlib import asynccontextmanager
from functools import partial
import strawberry
from strawberry.types import Info
from fastapi import FastAPI
from strawberry.fastapi import BaseContext, GraphQLRouter
from databases import Database

from app.settings import Settings


class Context(BaseContext):
    db: Database

    def __init__(
        self,
        db: Database,
    ) -> None:
        self.db = db



@strawberry.type
class Author:
    name: str


@strawberry.type
class Book:
    title: str
    author: Author


@strawberry.type
class Query:

    @strawberry.field
    async def books(
        self,
        info: Info[Context, None],
        author_ids: list[int] | None = [],
        search: str | None = None,
        limit: int | None = None,
    ) -> list[Book]:
        db = info.context.db

        query = """
            SELECT b.title, a.name
            FROM books b
            JOIN authors a ON b.author_id = a.id
        """

        conditions = []
        values: dict[str, object] = {}

        if author_ids:
            conditions.append("b.author_id = ANY(:author_ids)")
            values["author_ids"] = author_ids

        if search:
            conditions.append("b.title ILIKE :search")
            values["search"] = f"%{search}%"

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY b.title"

        if limit is not None:
            query += " LIMIT :limit"
            values["limit"] = limit

        rows = await db.fetch_all(query, values)

        return [
            Book(
                title=row["title"],
                author=Author(name=row["name"])
            )
            for row in rows
        ]



CONN_TEMPLATE = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"
settings = Settings()  # type: ignore
db = Database(
    CONN_TEMPLATE.format(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        port=settings.DB_PORT,
        host=settings.DB_SERVER,
        name=settings.DB_NAME,
    ),
)

@asynccontextmanager
async def lifespan(
    app: FastAPI,
    db: Database,
):
    async with db:
        yield
    await db.disconnect()

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(  # type: ignore
    schema,
    context_getter=partial(Context, db),
)

app = FastAPI(lifespan=partial(lifespan, db=db))
app.include_router(graphql_app, prefix="/graphql")
