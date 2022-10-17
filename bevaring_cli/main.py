import logging
from logging.handlers import RotatingFileHandler
from os.path import isfile
from typing import List

from bevaring_cli.commands.app import App
from enterprython import assemble, load_config
from rich.logging import RichHandler

from bevaring_cli import BEVARING_CLI_APP_NAME
from bevaring_cli.commands.cmd import Cmd
from bevaring_cli.config import SESSION_FILE

from bevaring_cli.commands import *  # need this for automatic command injection

consoleHandler = RichHandler(markup=True, show_path=False, show_time=False, show_level=False)
consoleHandler.setFormatter(logging.Formatter("%(message)s", style='%'))
fileHandler = RotatingFileHandler(BEVARING_CLI_APP_NAME + '.log', maxBytes=1_000_000, backupCount=3)
fileHandler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
logging.basicConfig(level=logging.INFO, handlers=[consoleHandler, fileHandler])  # Enable DEBUG log for entire script
logging.getLogger("msal").setLevel(logging.WARNING)  # Optionally disable MSAL DEBUG logs
log = logging.getLogger(__name__)


def all_cmds(cmds: List[Cmd]) -> Cmd:
    """Instantiates all command objects and return App instance (which is a command too)."""
    return next(cmd for cmd in cmds if type(cmd) == App)


def app() -> Cmd:
    paths = ["app.toml"]
    if isfile(SESSION_FILE):
        paths += SESSION_FILE
    load_config(app_name=BEVARING_CLI_APP_NAME.replace('-', '_'), paths=paths)
    return assemble(all_cmds)


if __name__ == "__main__":
    try:
        app().run()
    except (SystemExit, KeyboardInterrupt):
        raise
    except:
        log.exception("Command failed!")
        raise SystemExit(2)
