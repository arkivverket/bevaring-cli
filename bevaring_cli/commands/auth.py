import logging

import typer
from typer import Option

from bevaring_cli.commands.app import App
from enterprython import component

from bevaring_cli.commands.cmd import Cmd
from bevaring_cli.auth import Authentication

logger = logging.getLogger(__name__)


@component()
class AuthCmd(Cmd):

    def __init__(self, app: App, auth: Authentication):
        super().__init__()
        self._auth = auth
        self.register(self.login, self.logout, self.debug_jwt)
        app.add(self._app, name='auth', help='Login and logout for bevaring')

    def login(
        self,
        use_device_code: bool = Option(
            False,
            "--use-device-code",
            help="Use device code flow, suitable for when running the CLI on a machine "
                 "that does not have a browser installed.",
        ),
        endpoint: str = Option('', help=("The endpoint to use for the API. You might also overwrite default with e.g. "
            "export BEVARING_CLI_ENDPOINT=bevaring.dev.digitalarkivet.no"))
    ) -> None:
        """
        Login with Azure AD

        By default, this will use interactive authentication, but you can use the --device-code flag to use device code
        authentication, which is suitable for when running the CLI on a machine that does not have a browser installed.
        """
        result = None

        if use_device_code:
            result = self._auth.login_with_device_code()
        else:
            result = self._auth.login_interactive()

        if result:
            logger.info(f"Successfully logged in as [green]{result['username']}[/green]")

    def logout(self) -> None:
        """
        Logout from Azure AD
        """
        logger.info("Logging out...")
        self._auth.logout()

    def debug_jwt(
        self,
        yes: bool = typer.Option(
            False,
            "--yes",
            "-y",
            help="Do not prompt for confirmation",
        ),
    ) -> None:
        """
        Debug the JWT token
        """
        if not yes:
            typer.confirm("This will print the JWT token to the console. Do you want to continue?", abort=True)

        print(self._auth.get_credentials()["access_token"])
