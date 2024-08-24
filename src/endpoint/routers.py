from fastapi import FastAPI

from src.endpoint.views import api


def setup_routes(app: FastAPI) -> None:
    app.include_router(api.router)


__all__ = [
    'setup_routes'
]
