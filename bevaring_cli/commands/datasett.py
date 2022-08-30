import typer

from bevaring_cli.auth import Authentication
from bevaring_cli.utils import state

app = typer.Typer()


@app.callback()
def main(ctx: typer.Context):
    if ctx.invoked_subcommand != 'login':
        state["credentials"] = Authentication().get_credentials()


@app.command()
def list():
    import httpx
    from rich.console import Console
    from rich.table import Table
    console = Console()

    # Calling graph using the access token
    response = httpx.get(
        url=f"https://{state['endpoint']}/api/metadata/datasett?limit=2",
        headers={
            "Authorization": f"Bearer {state['credentials']['access_token']}",
        },
    )

    table = Table("Datasett ID", "Databehandler", "Merkelapp")
    for dataset in response.json()["result"]:
        table.add_row(
            dataset["datasett_id"],
            dataset["databehandler"],
            dataset["merkelapp"],
        )

    console.print(table)
