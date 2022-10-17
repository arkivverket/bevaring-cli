import logging
from __main__ import App, BEVARING_CLI_APP_NAME

from click import UUID
from enterprython import component
from rich.table import Table
from toml import dump
from typer import Argument

from bevaring_cli.bevaring_client import BevaringClient
from bevaring_cli.cmd import Cmd
from bevaring_cli.config import SESSION_FILE

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
        datasett_id: str = Argument(..., help="Identifier of the dataset to check out."),
        email: str = Argument(..., help="Email address where to send progress notification."),
        empty=True,
        debug=False
    ) -> None:
        json = self._bevaring().post(
            url='bevaring/checkout_dataset',
            data={
                'client_name': BEVARING_CLI_APP_NAME,
                'datasett_id': datasett_id,
                'with_data': not empty,
                'receipt_email': email
            }).json()
        with open(SESSION_FILE, 'w') as f:
            dump(json, f)
        if debug:
            table = Table("Datasett ID", "Session ID", "Bucket Name", "IAM Key", "IAM Secret")
            table.add_row(
                json['datasett_id'],
                json['session_id'],
                json['bucket_name'],
                json['iam_access_key_id'],
                json['iam_secret_access_key'],
            )
            log.info(table)
        log.info(f"Creation of the {json['bucket_name']} was triggered. Await email notification.")
