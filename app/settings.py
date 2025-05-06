import pydantic
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn
from urllib.parse import quote



class Settings(BaseSettings):
    DB_USER: str = pydantic.Field(alias="POSTGRES_USER")
    DB_PASSWORD: str = pydantic.Field(alias="POSTGRES_PASSWORD")
    DB_SERVER: str = pydantic.Field(alias="POSTGRES_HOST")
    DB_PORT: int = pydantic.Field(alias="POSTGRES_PORT")
    DB_NAME: str = pydantic.Field(alias="POSTGRES_DB_NAME")
    DATABASE_DSN: str = ""


    @pydantic.field_validator("DATABASE_DSN", mode="before")
    @classmethod
    def assemble_db_dsn(cls, _: str, values: pydantic.ValidationInfo) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=values.data["DB_USER"],
                password=quote(values.data["DB_PASSWORD"]),
                host=values.data["DB_SERVER"],
                port=values.data["DB_PORT"],
                path=f'{values.data["DB_NAME"]}',
            ),
        )

settings = Settings() # type: ignore [call-arg]