import logging
from functools import cache

from attrs import define
from enterprython import component, setting
from httpx import Client

from bevaring_cli.auth import Authentication

log = logging.getLogger(__name__)


@component()
@define
class BevaringClient:
    """Lazily initialized Bevaring rest API client. Contains authorization headers."""
    auth: Authentication
    endpoint: str = setting('ENDPOINT')

    @cache
    def __call__(self) -> Client:
        return Client(
            base_url=f'https://{self.endpoint}/api/',
            headers={'Authorization': f"Bearer {self.auth.get_credentials()['access_token']}"},
            event_hooks={'request': [lambda req: log.info(f"{req.url}\n{req.headers}\n{req._content}")]}
        )

    def __hash__(self) -> int:
        return hash(self.endpoint) + hash(self.auth)