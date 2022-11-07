import logging
from logging.handlers import RotatingFileHandler
from os.path import isfile, dirname
from typing import List

from bevaring_cli.commands.app import App
from enterprython import assemble, load_config
from rich.logging import RichHandler

from bevaring_cli import BEVARING_CLI_APP_NAME
from bevaring_cli.commands.cmd import Cmd
from bevaring_cli.config import SESSION_FILE

from bevaring_cli.commands import *  # noqa: F401,F403 need this for automatic command injection


console_handler = RichHandler(markup=True, show_path=False, show_time=False, show_level=False)
console_handler.setFormatter(logging.Formatter("%(message)s", style='%'))
file_handler = RotatingFileHandler(BEVARING_CLI_APP_NAME + '.log', maxBytes=1_000_000, backupCount=3)
file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
logging.basicConfig(level=logging.INFO, handlers=[console_handler, file_handler])  # Enable DEBUG log for entire script
logging.getLogger("msal").setLevel(logging.WARNING)  # Optionally disable MSAL DEBUG logs


def all_cmds(cmds: List[Cmd]) -> Cmd:
    """Instantiates all command objects and return App instance (which is a command too)."""
    return next(cmd for cmd in cmds if type(cmd) == App)


def app(profile='prod') -> Cmd:
    paths = [f"{dirname(__file__)}/app.toml"]
    if isfile(SESSION_FILE):
        paths.append(SESSION_FILE)
    load_config(app_name=BEVARING_CLI_APP_NAME.replace('-', '_'), paths=paths)
    if profile == 'prod':
        # TODO: Enterprython does not forward profile down component stack. So we have to simulate it here by importing
        # TODO: packages when necessary. Fix the bug in Enterprython.
        from bevaring_cli.auth_prod import AuthenticationProd  # noqa: F401
    return assemble(all_cmds)

if __name__ == "__main__":
    try:
        app().run()
    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Command failed!\n{str(e)}")
        raise SystemExit(2)
