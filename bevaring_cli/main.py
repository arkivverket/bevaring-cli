import logging
from logging.handlers import RotatingFileHandler
from typing import List

from enterprython import component, assemble, load_config
from rich.logging import RichHandler

from bevaring_cli import __version__, BEVARING_CLI_APP_NAME
from bevaring_cli.cmd import Cmd

consoleHandler = RichHandler(markup=True, show_path=False, show_time=False, show_level=False)
consoleHandler.setFormatter(logging.Formatter("%(message)s", style='%'))
fileHandler = RotatingFileHandler(BEVARING_CLI_APP_NAME + '.log', maxBytes=1_000_000, backupCount=3)
fileHandler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
logging.basicConfig(level=logging.INFO, handlers=[consoleHandler, fileHandler])  # Enable DEBUG log for entire script
logging.getLogger("msal").setLevel(logging.WARNING)  # Optionally disable MSAL DEBUG logs
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


def all_cmds(cmds: List[Cmd]) -> Cmd:
    for cmd in cmds:
        if type(cmd) == App:
            return cmd


if __name__ == "__main__":
    try:
        load_config(app_name=BEVARING_CLI_APP_NAME, paths=["app.toml"])
        assemble(all_cmds).run()
    except:
        log.exception("Command failed!")
        raise SystemExit(2)
