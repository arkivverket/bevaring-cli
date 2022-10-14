from attrs import define, field
from click import get_app_dir
from enterprython import component, setting, factory
from httpx import Client

from bevaring_cli import BEVARING_CLI_APP_NAME
from bevaring_cli.auth import Authentication


@component()
@define(frozen=True, on_setattr=None)
class Config:
    # setting() is just to ignore default CONFIG_ prefix.
    client_id: str = setting("CLIENT_ID")
    endpoint: str = setting("ENDPOINT")
    config_dir: str = field(init=False, factory=lambda: get_app_dir(app_name=BEVARING_CLI_APP_NAME))


@factory()
def bevaring_client(cfg: Config, auth: Authentication) -> Client:
    return Client(
        base_url=f'https://{cfg.endpoint}/api/metadata/',
        headers={"Authorization": f"Bearer {auth.get_credentials()['access_token']}"}
    )
