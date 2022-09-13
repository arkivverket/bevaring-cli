import typer

from rich import print

from bevaring_cli.auth import Authentication
from bevaring_cli.utils import state

app = typer.Typer()


@app.callback()
def main(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand != 'login':
        state["credentials"] = Authentication().get_credentials()


@app.command()
def login(
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
    auth = Authentication()
    result = None

    if use_device_code:
        result = auth.login_with_device_code()
    else:
        result = auth.login_interactive()

    if result:
        print(f"Successfully logged in as [green]{result['username']}[/green]")


@app.command()
def logout() -> None:
    """
    Login with Azure AD

    By default this will use interactive authentication, but you can use the --device-code flag to use device code authentication,
    which is suitable for when running the CLI on a machine that does not have a browser installed.
    """
    auth = Authentication()
    print("Logging out...")
    auth.logout()
