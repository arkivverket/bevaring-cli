import logging

from genericpath import isfile
from typing import List
from attrs import define
from enterprython import component
from enterprython._inject import ENTERPRYTHON_VALUE_STORE
from rich.console import Console
from rich.table import Table
from typer import Argument, Option
from toml import load, dump

from bevaring_cli import BEVARING_CLI_APP_NAME
from bevaring_cli.bevaring_client import BevaringClient
from bevaring_cli.commands.app import App
from bevaring_cli.commands.cmd import Cmd
from bevaring_cli.config import COPY_FILE
from bevaring_cli.exceptions import ensure_success
from bevaring_cli.commands.session import SessionCmd
aws_export = SessionCmd.aws_export

logger = logging.getLogger(__name__)


@component()
@define(slots=False)
class DatasettCmd(Cmd):

    _main: App
    _bevaring: BevaringClient

    def __attrs_post_init__(self):
        super().__init__()
        self.register(self.list, self.copies, self.copy, self.aws)
        self._main.add(self._app, name='datasett', help='Readonly utility for datasetts')

    def list(
        self,
        limit: int = Option(2, help="Max amount of datasetts to list"),
        endpoint: str = Option('', help=f"The endpoint to use for the API. Default is {ENTERPRYTHON_VALUE_STORE['ENDPOINT']}"),
    ) -> None:
        response = self._bevaring().get(f'metadata/datasett?limit={limit}')

        table = Table("Datasett ID", "Databehandler", "Merkelapp")
        for datasett in response.json()['result']:
            table.add_row(
                datasett['datasett_id'],
                datasett['databehandler'],
                datasett['merkelapp'],
            )
        Console().print(table)

    def copies(self):
        """Prints all locally stored credentials from copy operations."""
        if isfile(COPY_FILE):
            print("\n".join("id: {}\ttarget_s3_uri: {}".format(key, value['target_s3_uri']) for (key, value) in load(COPY_FILE).items()))
        else:
            print("No copy credentials file exists since no copies have been created yet.")

    def copy(
        self,
        datasett_id: str = Argument(..., help="Identifier of the datasett to copy"),
        id: str = Option(None, help="User defined id for locally stored credentials"),
        bucket_name: str = Option(None, help="Name of the target bucket. If not specified a temporary bucket will be created"),
        iam_access_key_id: str = Option(None, help="IAM access key id if user has a bucket"),
        iam_secret_access_key: str = Option(None, help="IAM secret access key if user has a bucket"),
        s3_path: str = Option(None, help="Root-folder within bucket where the datasett should be copied"),
        generation_name: str = Option(None, help="Which generation to copy"),
        receipt_email: str = Option(None, help="Email address for progress notifications"),
        endpoint: str = Option('', help=f"The endpoint to use for the API. Default is {ENTERPRYTHON_VALUE_STORE['ENDPOINT']}"),
    ) -> None:
        """Initiates copying of a chosen generation of a datasett into a target bucket. If the user has no bucket, a temporary bucket with credentials is created."""
        response = self._bevaring().post(
            url='bevaring/copy_dataset',
            json={
                'client_name': BEVARING_CLI_APP_NAME,
                'datasett_id': datasett_id,
                'bucket_name': bucket_name,
                'iam_access_key_id': iam_access_key_id,
                'iam_secret_access_key': iam_secret_access_key,
                's3_path': s3_path,
                'generation_name': generation_name,
                'receipt_email': receipt_email,
            }
        )
        ensure_success(response)
        json = response.json()

        if isfile(COPY_FILE):
            copies = load(COPY_FILE)
        else:
            copies = {}

        existing_ids = list(copies.keys())
        copies[self.next_id(id, existing_ids)] = {
            'target_s3_uri': json['target_s3_uri'],
            'iam_access_key_id': json['iam_access_key_id'],
            'iam_secret_access_key': json['iam_secret_access_key'],
        }
        self.persist(copies)

        if receipt_email:
            logger.info(f"Copying of datasett to bucket {json['bucket_name']} initiated. Await email notification.")
        else:
            logger.info(f"Copying of datasett to bucket {json['bucket_name']} initiated.")

    def aws(
        self,
        id: str = Argument(..., help="Id of the aws credentials to print"),
    ) -> None:
        try:
            copy = load(COPY_FILE)[id]
            aws_export(copy['iam_access_key_id'], copy['iam_secret_access_key'])
        except KeyError:
            print("The id was not found.")
            raise

    @staticmethod
    def next_id(id: str, existing_ids: List[str]):
        if id:
            if id not in existing_ids:
                return id
            else:
                raise KeyError("The id already exists.")
        else:
            next_id = 1
            while str(next_id) in existing_ids:
                next_id += 1
        return str(next_id)

    @staticmethod
    def persist(copies: dict) -> None:
        with open(COPY_FILE, 'w') as f:
            dump(copies, f)
