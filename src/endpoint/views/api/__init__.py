from fastapi import APIRouter

from src.endpoint.views.api import translation

router = APIRouter(
    prefix='/api',
    tags=['API Handlers'],
)

router.include_router(translation.router)

__all__ = [
    'router'
]
