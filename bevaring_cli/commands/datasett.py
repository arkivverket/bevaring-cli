from __main__ import App

from enterprython import component

from bevaring_cli.Cmd import Cmd
from bevaring_cli.auth import Authentication
from bevaring_cli.utils import state


@component()
class Datasett(Cmd):

    def __init__(self, app: App, auth: Authentication):
        super().__init__()
        self._auth = auth
        self.register(self.list)
        app.add(self._app, "datasett")

    def list(self) -> None:
        import httpx
        from rich.console import Console
        from rich.table import Table
        console = Console()

        # Calling graph using the access token
        response = httpx.get(
            url=f"https://{state['endpoint']}/api/metadata/datasett?limit=2",
            headers={
                "Authorization": f"Bearer {self._auth.get_credentials()['access_token']}",
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
