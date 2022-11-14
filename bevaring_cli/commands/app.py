import logging

from bevaring_cli import BEVARING_CLI_APP_NAME, __version__
from bevaring_cli.commands.cmd import Cmd
from enterprython import component

logger = logging.getLogger(__name__)

VERSION = f"{BEVARING_CLI_APP_NAME} version {__version__}"


@component()
class App(Cmd):

    def __init__(self):
        super().__init__()
        self.register(self.version)

    @staticmethod
    def version() -> None:
        """Prints the version"""
        logger.info(VERSION)
