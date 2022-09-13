import logging

from typer import Option, Typer

from bevaring_cli import __version__
from bevaring_cli.commands import auth, datasett
from bevaring_cli.utils import console, state

logging.basicConfig(level=logging.INFO)  # Enable DEBUG log for entire script
logging.getLogger("msal").setLevel(logging.WARNING)  # Optionally disable MSAL DEBUG logs
logger = logging.getLogger(__name__)

app = Typer()
app.add_typer(datasett.app, name="datasett")
app.add_typer(auth.app, name="auth")


@app.callback()
def main(
    endpoint: str = Option(
        state["endpoint"],
        help="The endpoint to use for the API",
    ),
) -> None:
    if endpoint:
        # Only inform the user if the endpoint is different from the default
        if state["endpoint"] != endpoint:
            console.print(f"Setting endpoint to [green]{endpoint}[/green]")
        state["endpoint"] = endpoint


@app.command()
def version() -> None:
    """Prints the version"""
    console.print(f"bevaring-cli version {__version__}")


if __name__ == "__main__":
    app()
