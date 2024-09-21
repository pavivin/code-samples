from fastapi import FastAPI

import src.app.auth.views as auth
import src.app.healthcheck.views as healthcheck
import src.app.balance.views as balance


def setup_routes(app: FastAPI) -> None:
    app.include_router(healthcheck.router, tags=["healthcheck"], prefix="/api")
    app.include_router(auth.router, tags=["auth"], prefix="/api")
    app.include_router(balance.router, tags=["items"], prefix="/api")
