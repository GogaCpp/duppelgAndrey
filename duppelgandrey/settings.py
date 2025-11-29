import logging

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(extra="ignore")

    debug: bool = True
    log_level: int = logging.DEBUG if debug else logging.INFO

    # tg
    api_id: int
    api_hash: str
    tg_token: str


settings = Settings(
    _env_file=(".env", ".env.dev", ".env.prod"),
    _env_file_encoding="utf-8",
)
