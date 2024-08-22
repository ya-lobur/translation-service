from logging import config

import uvloop
from typer import Typer

from src.config import settings
from src.endpoint.app import web_app

uvloop.install()
config.dictConfig(settings.LOGGING)
manager = Typer()


@manager.command('run_endpoint')
def run_endpoint(
    host: str = settings.HOST,
    port: int = settings.PORT,
) -> None:
    web_app.run(host=host, port=port)


if __name__ == '__main__':
    manager()

__all__ = [
    'manager'
]
