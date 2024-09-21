from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import ORJSONResponse

from src.app.core.middlewares import setup_middlewares
from src.db.base import create_db_and_tables

from src.app.core import exceptions
from src.app.core.protocol import Response
from src.config import settings
from src.logger import logger
from src.redis import Redis

from src.app.core.views import setup_routes


if not settings.DEBUG:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=0.75,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Redis().connect()
    await create_db_and_tables()
    yield
    await Redis().disconnect()


app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json", redoc_url=None, lifespan=lifespan)


setup_routes(app)
setup_middlewares(app)


@app.exception_handler(Exception)
async def uvicorn_base_exception_handler(request: Request, exc: Exception):
    sentry_sdk.capture_exception(exc)
    logger.error(exc)
    error = exceptions.ServerError(str(exc))
    return ORJSONResponse(
        Response(
            code=error.status_code,
            message=error.message,
            body=error.payload,
            exception_class=error.__class__.__name__,
        ).dict(),
        status_code=error.status_code,
    )


@app.exception_handler(exceptions.ApiException)
async def unicorn_api_exception_handler(request: Request, exc: exceptions.ApiException):
    logger.debug(str(exc))

    return ORJSONResponse(
        Response(
            code=exc.status_code,
            message=exc.message,
            body=exc.payload,
            exception_class=exc._type(),
        ).dict(),
        status_code=exc.status_code,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.debug(exc)
    error = exceptions.ValidationError(message=str(exc))
    return ORJSONResponse(
        Response(
            code=error.status_code,
            message=error.message,
            body=error.payload,
            exception_class=error._type(),
        ).dict(),
        status_code=error.status_code,
    )


@app.exception_handler(HTTPException)
async def validation_http_exception_handler(request: Request, exc: HTTPException):
    sentry_sdk.capture_exception(exc)
    logger.error(exc)
    error = exceptions.UnauthorizedError(message=str(exc))
    return ORJSONResponse(
        Response(
            code=error.status_code,
            message=error.message,
            body=error.payload,
            exception_class=error._type(),
        ).dict(),
        status_code=error.status_code,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=settings.BACKEND_HOST, port=settings.BACKEND_PORT, workers=settings.WORKERS_COUNT)
