import logging
from __main__ import App

from click import UUID
from enterprython import component
from rich.table import Table
from typer import Argument

from bevaring_cli.bevaring_client import BevaringClient
from bevaring_cli.cmd import Cmd

log = logging.getLogger(__name__)


@component()
class DatasettCmd(Cmd):

    def __init__(self, app: App, bevaring: BevaringClient):
        super().__init__()
        self._bevaring = bevaring
        self.register(self.list)
        self.register(self.checkout)
        app.add(self._app, "datasett")

    def list(self) -> None:
        response = self._bevaring().get('metadata/datasett?limit=2')

        table = Table("Datasett ID", "Databehandler", "Merkelapp")
        for dataset in response.json()["result"]:
            table.add_row(
                dataset["datasett_id"],
                dataset["databehandler"],
                dataset["merkelapp"],
            )

        log.info(table)

    def checkout(
        self,
        dattasett_id: UUID = Argument(..., help=""),
        client: str = Argument(..., help=""),
        email: str = Argument(..., help=""),
        empty=True
    ) -> None:
        json = self._bevaring().post(
            url='bevaring/checkout_dataset',
            data={
                'client_name': client,
                'datasett_id': str(dattasett_id),
                'with_data': not empty,
                'receipt_email': email
            }).json()

        table = Table("Datasett ID", "Session ID", "Bucket Name", "IAM Key", "IAM Secret")
        table.add_row(
            json["datasett_id"],
            json["session_id"],
            json["bucket_name"],
            json["iam_access_key_id"],
            json["iam_secret_access_key"],
        )
        log.info(table)
