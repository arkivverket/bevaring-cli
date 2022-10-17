import logging

from bevaring_cli import BEVARING_CLI_APP_NAME, __version__
from bevaring_cli.commands.cmd import Cmd
from enterprython import component

log = logging.getLogger(__name__)


@component()
class App(Cmd):

    def __init__(self):
        super().__init__()
        self.register(self.version)

    @staticmethod
    def version() -> None:
        """Prints the version"""
        log.info(f"{BEVARING_CLI_APP_NAME} version {__version__}")

