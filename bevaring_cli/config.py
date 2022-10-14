from attrs import define, field
from click import get_app_dir
from enterprython import component, setting

from bevaring_cli import BEVARING_CLI_APP_NAME


@component()
@define(frozen=True, on_setattr=None)
class Config:
    # setting() is just to ignore default CONFIG_ prefix.
    client_id: str = setting("CLIENT_ID")
    endpoint: str = setting("ENDPOINT")
    config_dir: str = field(init=False, factory=lambda: get_app_dir(app_name=BEVARING_CLI_APP_NAME))
