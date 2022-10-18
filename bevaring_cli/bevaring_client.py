from functools import cache

from enterprython import component
from httpx import Client

from bevaring_cli.auth import Authentication
from bevaring_cli.config import Config


@component()
class BevaringClient:
    """Lazily initialized Bevaring rest API client. Contains authorization headers."""

    def __init__(self, cfg: Config, auth: Authentication):
        self.cfg = cfg
        self.auth = auth

    @cache
    def __call__(self) -> Client:
        return Client(
            base_url=f'https://{self.cfg.endpoint}/api/',
            headers={'Authorization': f"Bearer {self.auth.get_credentials()['access_token']}"}
        )
