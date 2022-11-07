from typing import Callable

from typer import Typer


class Cmd:

    def __init__(self):
        self._app = Typer()

    def register(self, *args: Callable, **kwargs: Callable) -> None:
        for cmd in args:
            self._app.command()(cmd)
        for name, cmd in kwargs:
            self._app.command(name)(cmd)

    def callback(self, cmd: Callable) -> None:
        self._app.callback()(cmd)

    def add(self, sub: Typer, name: str = None, help: str = None) -> None:
        self._app.add_typer(sub, name=name, help=help)

    def run(self) -> None:
        self._app()
