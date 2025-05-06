from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from functools import partial
from contextlib import asynccontextmanager

from app.database import db
from app.graphql.schema import schema
from app.graphql.context import Context


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()


graphql_app: GraphQLRouter = GraphQLRouter(
    schema,
    context_getter=partial(Context, db)
)

app = FastAPI(lifespan=lifespan)
app.include_router(graphql_app, prefix="/graphql")
