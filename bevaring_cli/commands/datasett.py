import logging

from attrs import define
from enterprython import component
from rich.console import Console
from rich.table import Table
from typer import Option

from bevaring_cli.bevaring_client import BevaringClient
from bevaring_cli.commands.app import App
from bevaring_cli.commands.cmd import Cmd

logger = logging.getLogger(__name__)


@component()
@define(slots=False)
class DatasettCmd(Cmd):

    _main: App
    _bevaring: BevaringClient

    def __attrs_post_init__(self):
        super().__init__()
        self.register(self.list)
        self._main.add(self._app, name='datasett', help='Readonly utility for datasetts.')

    def list(
        self,
        limit: int = Option(2, help="Max amount of datasets to list"),
        endpoint: str = Option('', help="The endpoint to use for the API")
    ) -> None:
        response = self._bevaring().get(f'metadata/datasett?limit={limit}')

        table = Table("Datasett ID", "Databehandler", "Merkelapp")
        for dataset in response.json()['result']:
            table.add_row(
                dataset['datasett_id'],
                dataset['databehandler'],
                dataset['merkelapp'],
            )

        Console().print(table)
