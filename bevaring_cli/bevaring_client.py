from functools import cache

from attrs import define
from enterprython import component, setting
from httpx import Client

from bevaring_cli.auth import Authentication


@component()
@define(hash=True)
class BevaringClient:
    """Lazily initialized Bevaring rest API client. Contains authorization headers."""
    auth: Authentication
    endpoint: str = setting('ENDPOINT')

    @cache
    def __call__(self) -> Client:
        return Client(
            base_url=f'https://{self.endpoint}/api/',
            headers={'Authorization': f"Bearer {self.auth.get_credentials()['access_token']}"}
        )
