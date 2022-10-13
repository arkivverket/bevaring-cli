from __main__ import App

import typer
from enterprython import component

from bevaring_cli.Cmd import Cmd
from bevaring_cli.auth import Authentication
from bevaring_cli.utils import console


@component()
class AuthCmd(Cmd):

    def __init__(self, app: App, auth: Authentication):
        super().__init__()
        self._auth = auth
        self.register(self.login, self.logout)
        app.add(self._app, "auth")

# @app.callback()
# def main(ctx: typer.Context) -> None:
#     if ctx.invoked_subcommand != 'login':
#         state["credentials"] = Authentication().get_credentials()

    def login(
        self,
        use_device_code: bool = typer.Option(
            False,
            "--use-device-code",
            help="Use device code flow, suitable for when running the CLI on a machine that does not have a browser installed.",
        ),
    ) -> None:
        """
        Login with Azure AD

        By default this will use interactive authentication, but you can use the --device-code flag to use device code authentication,
        which is suitable for when running the CLI on a machine that does not have a browser installed.
        """
        result = None

        if use_device_code:
            result = self._auth.login_with_device_code()
        else:
            result = self._auth.login_interactive()

        if result:
            console.print(f"Successfully logged in as [green]{result['username']}[/green]")

    def logout(self) -> None:
        """
        Logout from Azure AD
        """
        console.print("Logging out...")
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
