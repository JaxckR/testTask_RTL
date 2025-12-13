from dataclasses import dataclass
from functools import cached_property
from os import getenv
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parents[2]


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
class LLMConfig:
    OPENROUTER_TOKEN: str

    @cached_property
    def prompt(self) -> str:
        with open(f"{BASE_PATH.parent}/llm_prompt.txt", "r") as f:
            return f.read()


@dataclass(frozen=True)
class Config:
    BOT_TOKEN: str
    llm: LLMConfig
    postgres: PostgresConfig


config = Config(
    BOT_TOKEN=getenv("BOT_TOKEN"),
    llm=LLMConfig(
        OPENROUTER_TOKEN=getenv("OPENROUTER_TOKEN"),
    ),
    postgres=PostgresConfig(
        user=getenv("POSTGRES_USER"),
        password=getenv("POSTGRES_PASSWORD"),
        host=getenv("POSTGRES_HOST"),
        database=getenv("POSTGRES_DB"),
        port=int(getenv("POSTGRES_PORT")),
    ),
)
