import logging
from sys import stdout

import msal
from attrs import define
from enterprython import component, setting
from enterprython._inject import ENTERPRYTHON_VALUE_STORE
from msal_extensions import FilePersistence, PersistedTokenCache

from bevaring_cli import (
    BEVARING_CLI_APP_NAME,
    __version__,
)
from bevaring_cli.auth import Authentication
from bevaring_cli.config import CONFIG_DIR, DEFAULTS
from bevaring_cli.exceptions import AuthenticationError

ENDPOINT = 'ENDPOINT'
CLIENT_ID = 'd18685f9-148d-4e9a-98b3-194bcd01bc95'

logger = logging.getLogger(__name__)


@component()
@define(hash=True)
class AuthenticationProd(Authentication):
    """
    We use the prefix _msal to identify variables and methods used for the MSAL library
    """
    _msal_app_instance = None

    endpoint: str = setting(ENDPOINT)

    def __attrs_post_init__(self) -> None:
        self.authority = "https://login.microsoftonline.com/organizations"
        self.scopes = [f"https://{self.endpoint}/User.Login"]

    @property
    def _msal_app_kwargs(self) -> dict:
        token_cache = PersistedTokenCache(FilePersistence(f"{CONFIG_DIR}/msal_token_cache.json"))
        return {
            "token_cache": token_cache,
            "authority": self.authority,
            "app_name": BEVARING_CLI_APP_NAME,
            "app_version": __version__,
        }

    @property
    def _msal_app(self) -> msal.PublicClientApplication:
        """
        Returns the MSAL application object
        """
        if ENTERPRYTHON_VALUE_STORE['ENDPOINT'] != self.endpoint and stdout.isatty():
            logger.warning("Setting endpoint to [green]%s[/green]", self.endpoint)
        if not self._msal_app_instance:
            self._msal_app_instance = msal.PublicClientApplication(client_id=CLIENT_ID, **self._msal_app_kwargs)

        return self._msal_app_instance

    def login_interactive(self) -> dict:
        """
        Acquires a token for the application
        """
        logger.info("A web browser has been opened at "
                    "https://login.microsoftonline.com/organizations/oauth2/v2.0/authorize.")
        logger.info("Please continue the login in the web browser. "
                    "If no web browser is available or if the web browser fails to open, "
                    "use device code flow with `bevaring auth login --use-device-code`.")

        result = self._msal_app.acquire_token_interactive(scopes=self.scopes)
        return Authentication.validate_result(result)

    def login_with_device_code(self) -> dict:
        """
        Acquires a token for the application
        """
        flow = self._msal_app.initiate_device_flow(scopes=self.scopes)
        if "user_code" not in flow:
            raise ValueError("Could not initiate device flow")

        logger.info(
            f"To sign in, use a web browser to open the page {flow['verification_uri']} and "
            "enter the code [bold green]{flow['user_code']}[/bold green] to authenticate."
        )

        result = self._msal_app.acquire_token_by_device_flow(flow)
        return Authentication.validate_result(result)

    def logout(self) -> None:
        users = self._msal_app.get_accounts()

        for user in users:
            self._msal_app.remove_account(user)

    def get_credentials(self) -> dict:
        accounts = self._msal_app.get_accounts()
        if not accounts:
            logger.error("[red]Not logged in, please login[/red]")
            raise AuthenticationError()

        # We only support one account at the moment
        account = accounts[0]

        result = self._msal_app.acquire_token_silent(scopes=self.scopes, account=account)
        return Authentication.validate_result(result)
