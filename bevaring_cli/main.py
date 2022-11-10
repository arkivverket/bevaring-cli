import logging
import re
from importlib import import_module
from logging.handlers import RotatingFileHandler
from os.path import isfile, dirname, join
from typing import List

from toml import load

from bevaring_cli.commands.app import App
from enterprython import assemble, load_config
from rich.logging import RichHandler

from bevaring_cli import BEVARING_CLI_APP_NAME
from bevaring_cli.commands.cmd import Cmd
from bevaring_cli.config import COPY_FILE, CREDENTIALS_FILE, SESSION_FILE, CONFIG_DIR, DEFAULTS

from glob import glob


console_handler = RichHandler(markup=True, show_path=False, show_time=False, show_level=False)
console_handler.setFormatter(logging.Formatter("%(message)s", style='%'))
file_handler = RotatingFileHandler(CONFIG_DIR + '/' + BEVARING_CLI_APP_NAME + '.log', maxBytes=1_000_000, backupCount=3)
file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
logging.basicConfig(level=logging.INFO, handlers=[console_handler, file_handler])  # Enable DEBUG log for entire script
logging.getLogger("msal").setLevel(logging.WARNING)  # Optionally disable MSAL DEBUG logs


def all_cmds(cmds: List[Cmd]) -> Cmd:
    """Instantiates all command objects and return App instance (which is a command too)."""
    return next(cmd for cmd in cmds if type(cmd) == App)


def import_components(predicate) -> None:
    component = re.compile('^@component', flags=re.MULTILINE)
    base = dirname(__file__)
    base_len = len(dirname(base)) + 1
    for file in glob(join(base, "**/[a-z]*.py"), recursive=True):
        with open(file) as f:
            if component.search(f.read()) and predicate(file):
                import_module(file[base_len:-3].replace('/', '.'))


def app(profile='prod') -> Cmd:
    paths = [f"{dirname(__file__)}/app.toml"]
    if isfile(SESSION_FILE):
        paths.append(SESSION_FILE)
    load_config(app_name=BEVARING_CLI_APP_NAME.replace('-', '_'), paths=paths)
    # TODO: Enterprython does not forward profile down component stack. So we have to simulate it here by importing
    # TODO: packages when necessary. Fix the bug in Enterprython.
    import_components(lambda file: not file.endswith('_prod') or profile == 'prod')
    for path in paths:
        for key, value in load(path).items():
            DEFAULTS[key] = value
    return assemble(all_cmds)


def main():
    """
    Main application entry point used when running as python module or pipx executable
    (see pyproject.toml[tool.poetry.scripts]).
    """
    try:
        app().run()
    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Command failed!\n{str(e)}")
        raise SystemExit(getattr(e, 'exit_code', 2))


if __name__ == "__main__":
    main()
