import logging
import msal
from rich import print

from bevaring_cli import BEVARING_CLI_CLIENT_ID, __version__
from bevaring_cli.utils import state

logger = logging.getLogger(__name__)


class Authentication:
    """
    We use the prefix _msal to identify variables and methods used for the MSAL library
    """
    _msal_app_instance = None

    def __init__(self):
        self.client_id = BEVARING_CLI_CLIENT_ID
        self.authority = "https://login.microsoftonline.com/99d3d298-60cf-4636-9772-4a191b6f0d94"
        self.scopes = [
            self._scope_builder("User.Login"),
        ]

    @property
    def _msal_app(self):
        """
        Returns the MSAL application object
        """
        if not self._msal_app_instance:
            self._msal_app_instance = msal.PublicClientApplication(
                client_id=self.client_id,
                authority=self.authority,
                app_version=__version__,
                app_name="Bevaring CLI",
            )

        return self._msal_app_instance

    def login_interactive(self):
        """
        Acquires a token for the application
        """
        return self._msal_app.acquire_token_interactive(scopes=self.scopes)

    def login_with_device_code(self):
        """
        Acquires a token for the application
        """
        flow = self._msal_app.initiate_device_flow(scopes=self.scopes)
        if "user_code" not in flow:
            raise ValueError("Could not initiate device flow")

        print(
            f"To sign in, use a web browser to open the page {flow['verification_uri']} and enter the code [bold green]{flow['user_code']}[/bold green] to authenticate."
        )

        return self._msal_app.acquire_token_by_device_flow(flow)

    def _scope_builder(self, scope_name) -> str:
        return f"https://{state['endpoint']}/{scope_name}"
