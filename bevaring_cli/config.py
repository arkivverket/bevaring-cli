from click import get_app_dir

from bevaring_cli import BEVARING_CLI_APP_NAME

CONFIG_DIR = get_app_dir(app_name=BEVARING_CLI_APP_NAME)
SESSION_FILE = f"{CONFIG_DIR}/session.toml"
CREDENTIALS_FILE = '~/.aws/credentials'
