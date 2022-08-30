from functools import cache

from typer import get_app_dir

from bevaring_cli import BEVARING_CLI_APP_NAME

# @TODO: replace this with production values
state = {"endpoint": "bevaring.dev.digitalarkivet.no"}


@cache
def get_config_directory() -> str:
    return get_app_dir(app_name=BEVARING_CLI_APP_NAME)
