import logging
import textwrap

from attrs import define
from enterprython import component, setting
from msal_extensions import FilePersistence
from rich.console import Console
from rich.table import Table
from toml import dump
from typer import Argument, Option

from bevaring_cli import BEVARING_CLI_APP_NAME
from bevaring_cli.bevaring_client import BevaringClient
from bevaring_cli.commands.app import App
from bevaring_cli.commands.cmd import Cmd
from bevaring_cli.config import SESSION_FILE, CREDENTIALS_FILE
from bevaring_cli.exceptions import ensure_success

logger = logging.getLogger(__name__)


@component()
@define(slots=False)
class DatasettCmd(Cmd):

    _main: App
    _bevaring: BevaringClient
    datasett_id: str = setting('DATASETT_ID')
    session_id: str = setting('SESSION_ID')
    bucket_name: str = setting('BUCKET_NAME')
    iam_access_key_id: str = setting('IAM_ACCESS_KEY_ID')
    iam_secret_access_key: str = setting('IAM_SECRET_ACCESS_KEY')

    def __attrs_post_init__(self):
        super().__init__()
        self.register(self.list, self.checkout)
        self._main.add(self._app, 'datasett')

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

    def checkout(
        self,
        datasett_id: str = Argument(..., help="Identifier of the dataset to check out."),
        email: str = Argument(..., help="Email address where to send progress notification."),
        empty: bool = Option(True, help="If true check out empty bucket"),
        debug: bool = Option(False, help="Print complete response to console"),
        endpoint: str = Option('', help="The endpoint to use for the API")
    ) -> None:
        """Checks out given dataset into by default empty bucket. Response will be saved into hidden file."""

        if self.session_id:
            raise Exception(f"You have an opened session ({self.session_id}). Please close it first.")

        response = self._bevaring().post(
            url='bevaring/checkout_dataset',
            json={
                'client_name': BEVARING_CLI_APP_NAME,
                'datasett_id': datasett_id,
                'with_data': not empty,
                'receipt_email': email
            }
        )

        ensure_success(response)
        json = response.json()

        if 'bucket_name' in json:
            with open(SESSION_FILE, 'w') as f:
                dump(json, f)
            creds = FilePersistence(CREDENTIALS_FILE)
            creds.save(textwrap.dedent(f"""
                [default]
                aws_secret_access_key = {json['iam_access_key_id']}
                aws_access_key_id = {json['iam_secret_access_key']}
                """))
            if debug:
                table = Table("Datasett ID", "Session ID", "Bucket Name", "IAM Key", "IAM Secret")
                table.add_row(
                    json['datasett_id'],
                    json['session_id'],
                    json['bucket_name'],
                    json['iam_access_key_id'],
                    json['iam_secret_access_key'],
                )
                Console().print(table)
            logger.info(f"Creation of the {json['bucket_name']} was triggered. Await email notification.")
