from pathlib import Path
from typing import Any, Mapping, Optional

from pydantic import BaseSettings, PostgresDsn, validator

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    tasks_name = "test-tasks"

    DEBUG: bool = False

    SECRET_KEY = "secret"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DATABASE: str
    POSTGRES_TEST_DATABASE: str = ""
    DATABASE_URL: PostgresDsn = ""
    TEST_DATABASE_URL: PostgresDsn = ""
    ALEMBIC_DATABASE_URL: PostgresDsn = ""

    SERVER_PORT: int = 8000
    SERVER_HOST: str = "0.0.0.0"

    REDIS_URL: str = "redis://localhost:6379"

    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_BACKEND_URL: str = "redis://localhost:6379/1"

    AUTH_ALGORITHM: str = "HS256"  # RS256 more secure for sure
    ACCESS_TOKEN_EXPIRES: int = 30 * 60
    REFRESH_TOKEN_EXPIRES = 60 * 60 * 24 * 30

    DEFAULT_PAGE_SIZE = 20

    RAW_OBSCENE_WORDS_FILE = "obscene_words.txt"
    NORMALIZED_OBSCENE_WORDS_FILE = "normalized_words.txt"

    ALLOWED_PHOTO_TYPES = {"jpg", "jpeg", "png", "webp"}
    ALLOWED_VIDEO_TYPES = {"webp", "gif", "mp4", "mov", "aiff"}
    ALLOWED_MODEL_TYPES = {"gltf", "glb"}
    ALLOWED_UPLOAD_TYPES = ALLOWED_PHOTO_TYPES | ALLOWED_VIDEO_TYPES | ALLOWED_MODEL_TYPES

    FILE_MAX_SIZE_MB: int = 10
    FILE_MAX_SIZE_KB: int = 1024 * 1024 * FILE_MAX_SIZE_MB

    SENTRY_DSN: str = None

    # S3
    S3_ENDPOINT_URL: str | None = None
    S3_AWS_ACCESS_KEY_ID: str | None = None
    S3_AWS_SECRET_ACCESS_KEY: str | None = None
    BUCKET_NAME: str | None = None
    REGION_NAME: str | None = None

    RESULT_BACKEND = "redis://localhost:6379/"
    BROKER_URL = "amqp://rmuser:rmpassword@localhost:5672/"

    WORKERS_COUNT = 1
    BACKEND_PORT = 5000
    BACKEND_HOST = "0.0.0.0"

    @validator("DATABASE_URL", pre=True)
    def assemble_postgres_db_url(cls, v: Optional[str], values: Mapping[str, Any]) -> str:
        if v and isinstance(v, str):
            return v

        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                user=values["POSTGRES_USER"],
                password=values["POSTGRES_PASSWORD"],
                host=values["POSTGRES_HOST"],
                port=str(values["POSTGRES_PORT"]),
                path=f'/{values["POSTGRES_DATABASE"]}',
            )
        )

    @validator("ALEMBIC_DATABASE_URL", pre=True)
    def assemble_alembic_database_url(cls, v: Optional[str], values: Mapping[str, Any]) -> str:
        if v and isinstance(v, str):
            return v

        return str(
            PostgresDsn.build(
                scheme="postgresql+psycopg2",
                user=values["POSTGRES_USER"],
                password=values["POSTGRES_PASSWORD"],
                host=values["POSTGRES_HOST"],
                port=str(values["POSTGRES_PORT"]),
                path=f'/{values["POSTGRES_DATABASE"]}',
            )
        )

    @validator("TEST_DATABASE_URL", pre=True)
    def assemble_test_postgres_url(cls, v: Optional[str], values: Mapping[str, Any]) -> str:
        if not values.get("POSTGRES_TEST_DATABASE"):
            return ""
        if v and isinstance(v, str):
            return v

        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                user=values["POSTGRES_USER"],
                password=values["POSTGRES_PASSWORD"],
                host=values["POSTGRES_HOST"],
                port=str(values["POSTGRES_PORT"]),
                path=f'/{values["POSTGRES_TEST_DATABASE"]}',
            )
        )

    class Config:
        env_file = ".env"


settings = Settings()
