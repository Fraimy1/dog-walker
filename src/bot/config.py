from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    database_url: str = "sqlite+aiosqlite:///data/dog_walker.db"
    allowed_users: list[int] = []

    model_config = {"env_file": ".env"}


settings = Settings()
