import logging
from __main__ import App

from enterprython import component
from httpx import Client

from bevaring_cli.cmd import Cmd

log = logging.getLogger(__name__)


@component()
class DatasettCmd(Cmd):

    def __init__(self, app: App, bevaring: Client):
        super().__init__()
        self._bevaring = bevaring
        self.register(self.list)
        app.add(self._app, "datasett")

    def list(self) -> None:
        from rich.table import Table

        # Calling graph using the access token
        response = self._bevaring.get('datasett?limit=2')

        table = Table("Datasett ID", "Databehandler", "Merkelapp")
        for dataset in response.json()["result"]:
            table.add_row(
                dataset["datasett_id"],
                dataset["databehandler"],
                dataset["merkelapp"],
            )

        log.info(table)
