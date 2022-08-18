from typer import Typer

from bevaring_cli import __version__

app = Typer()


@app.command()
def version():
    """Prints the version"""
    print(f"bevaring-cli version {__version__}")


if __name__ == "__main__":
    app()
