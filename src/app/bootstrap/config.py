from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True)
class PostgresConfig:
    user: str
    password: str
    host: str
    database: str
    port: int

    @property
    def url(self) -> str:
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass(frozen=True)
class Config:
    BOT_TOKEN: str
    OPENROUTER_TOKEN: str
    postgres: PostgresConfig


config = Config(
    BOT_TOKEN=getenv("BOT_TOKEN"),
    OPENROUTER_TOKEN=getenv("OPENROUTER_TOKEN"),
    postgres=PostgresConfig(
        user=getenv("POSTGRES_USER"),
        password=getenv("POSTGRES_PASSWORD"),
        host=getenv("POSTGRES_HOST"),
        database=getenv("POSTGRES_DB"),
        port=int(getenv("POSTGRES_PORT")),
    ),
)
