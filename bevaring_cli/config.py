from os import makedirs
from typing import Dict

from click import get_app_dir

from bevaring_cli import BEVARING_CLI_APP_NAME

CONFIG_DIR = get_app_dir(app_name=BEVARING_CLI_APP_NAME)
makedirs(CONFIG_DIR, exist_ok=True)
SESSION_FILE = f"{CONFIG_DIR}/session.toml"
COPY_FILE = f"{CONFIG_DIR}/copy.toml"
DEFAULTS: Dict[str, str] = {}
