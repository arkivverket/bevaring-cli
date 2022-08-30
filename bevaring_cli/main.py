import logging

from rich import print
from typer import Typer, Option

from bevaring_cli import __version__
from bevaring_cli.auth.authentication import Authentication
from bevaring_cli.utils import state

logging.basicConfig(level=logging.INFO)  # Enable DEBUG log for entire script
logging.getLogger("msal").setLevel(logging.WARNING)  # Optionally disable MSAL DEBUG logs
logger = logging.getLogger(__name__)

app = Typer()


@app.callback()
def main(endpoint: str | None = None):
    if endpoint:
        state["endpoint"] = endpoint


@app.command()
def version():
    """Prints the version"""
    print(f"bevaring-cli version {__version__}")


@app.command()
def login(
    use_device_code: bool = Option(
        False,
        "--use-device-code",
        help="Use device code flow, suitable for when running the CLI on a machine that does not have a browser installed.",
    )
):
    """
    Login to Azure AD

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
def bevaring():
    import httpx
    auth = Authentication()
    result = auth.get_credentials()

    # Calling graph using the access token
    response = httpx.get(
        url=f"https://{state['endpoint']}/api/metadata/datasett?limit=2",
        headers={
            "Authorization": f"Bearer {result['access_token']}",
        },
    )
    print(response.json())


if __name__ == "__main__":
    app()
