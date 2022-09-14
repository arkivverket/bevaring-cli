import typer

from bevaring_cli.auth import Authentication
from bevaring_cli.utils import console, state

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
        console.print(f"Successfully logged in as [green]{result['username']}[/green]")


@app.command()
def logout() -> None:
    """
    Logout from Azure AD
    """
    auth = Authentication()
    console.print("Logging out...")
    auth.logout()


@app.command()
def debug_jwt(
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
    auth = Authentication()
    if not yes:
        typer.confirm("This will print the JWT token to the console. Do you want to continue?", abort=True)

    print(auth.get_credentials()["access_token"])
