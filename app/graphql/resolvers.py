import strawberry
from strawberry.types import Info
from typing import Optional
from app.graphql.context import Context


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
        author_ids: Optional[list[int]] = None,
        search: Optional[str] = None,
        limit: Optional[int] = None,
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
