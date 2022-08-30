import logging
import msal

from msal_extensions import FilePersistence, PersistedTokenCache
from rich import print

from bevaring_cli import (
    BEVARING_CLI_APP_NAME,
    BEVARING_CLI_CLIENT_ID,
    BEVARING_CLI_TENANT_ID,
    __version__,
)
from bevaring_cli.utils import validate_result
from bevaring_cli.exceptions import AuthenticationError
from bevaring_cli.utils import get_config_directory, state

logger = logging.getLogger(__name__)


class Authentication:
    """
    We use the prefix _msal to identify variables and methods used for the MSAL library
    """
    _msal_app_instance = None

    def __init__(self) -> None:
        self.client_id = BEVARING_CLI_CLIENT_ID
        self.authority = f"https://login.microsoftonline.com/{BEVARING_CLI_TENANT_ID}"
        self.scopes = [
            self._scope_builder("User.Login"),
        ]

    @property
    def _msal_app_kwargs(self) -> dict:
        token_cache = PersistedTokenCache(
            FilePersistence(
                f"{get_config_directory()}/msal_token_cache.json"
            )
        )
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
        if not self._msal_app_instance:
            self._msal_app_instance = msal.PublicClientApplication(client_id=self.client_id, **self._msal_app_kwargs)

        return self._msal_app_instance

    def login_interactive(self) -> dict:
        """
        Acquires a token for the application
        """
        result = self._msal_app.acquire_token_interactive(scopes=self.scopes)
        return validate_result(result)

    def login_with_device_code(self) -> dict:
        """
        Acquires a token for the application
        """
        flow = self._msal_app.initiate_device_flow(scopes=self.scopes)
        if "user_code" not in flow:
            raise ValueError("Could not initiate device flow")

        print(
            f"To sign in, use a web browser to open the page {flow['verification_uri']} and enter the code [bold green]{flow['user_code']}[/bold green] to authenticate."
        )

        result = self._msal_app.acquire_token_by_device_flow(flow)
        return validate_result(result)

    def get_credentials(self) -> dict:
        accounts = self._msal_app.get_accounts()
        if not accounts:
            print("[red]Not logged in, please login with:[/red]\nbevaring login")
            raise AuthenticationError()

        # We only support one account at the moment
        account = accounts[0]

        result = self._msal_app.acquire_token_silent(scopes=self.scopes, account=account)
        return validate_result(result)

    def _scope_builder(self, scope_name: str = None) -> str:
        if not scope_name:
            raise ValueError("Scope name is required")

        return f"https://{state['endpoint']}/{scope_name}"
