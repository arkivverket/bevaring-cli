import logging
import requests

from rich import print
from typer import Typer, Option

from bevaring_cli import __version__
from bevaring_cli.auth.core import Authentication

logging.basicConfig(level=logging.INFO)  # Enable DEBUG log for entire script
logging.getLogger("msal").setLevel(logging.INFO)  # Optionally disable MSAL DEBUG logs

app = Typer()
# @TODO: replace this with production values
state = {"endpoint": "bevaring.dev.digitalarkivet.no"}


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
    scopes = [f"https://{state['endpoint']}/User.Login"]

    if use_device_code:
        result = auth.login_with_device_code(scopes)
    else:
        result = auth.login_interactive(scopes)

    if "access_token" in result:
        # Calling graph using the access token
        response = requests.get(
            url=f"https://{state['endpoint']}/api/metadata/datasett?limit=1",
            allow_redirects=False,
            headers={
                "Authorization": f"Bearer {result['access_token']}",
            },
        )
        print(f"Response HTTP Status Code: {response.status_code}")
        print(response.content.decode('utf-8'))
    else:
        logging.error(result.get("error"))
        logging.error(result.get("error_description"))
        logging.error(result.get("correlation_id"))  # You may need this when reporting a bug


if __name__ == "__main__":
    app()
