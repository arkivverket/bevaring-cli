import logging
from typing import Any, List
import toml

from attrs import define
from enterprython import component
from msal_extensions import FilePersistence
from rich.console import Console
from rich.table import Table
from typer import Argument, Option

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
        self.register(self.list, self.copy, self.aws)
        self._main.add(self._app, name='datasett', help='Readonly utility for datasetts.')

    def list(
        self,
        limit: int = Option(2, help="Max amount of datasetts to list"),
        copies: bool = Option(None, help="Prints all locally stored credentials from copy operations"),
        endpoint: str = Option('', help="The endpoint to use for the API")
    ) -> None:
        if copies:
            copy_credentials = FilePersistence(COPY_FILE)
            content = copy_credentials.load()
            print(content)
        else:
            response = self._bevaring().get(f'metadata/datasett?limit={limit}')

            table = Table("Datasett ID", "Databehandler", "Merkelapp")
            for datasett in response.json()['result']:
                table.add_row(
                    datasett['datasett_id'],
                    datasett['databehandler'],
                    datasett['merkelapp'],
                )
            Console().print(table)

    def copy(
        self,
        datasett_id: str = Argument(..., help="Identifier of the datasett to copy."),
        user_has_bucket: bool = Argument(False, help="If user has a target bucket to copy to."),
        id: str = Option(None, help="User defined id for locally stored credentials."),
        bucket_name: str = Option(None, help="Name of the target bucket."),
        iam_access_key_id: str = Option(None, help="IAM acces key id if user has a bucket."),
        iam_secret_access_key: str = Option(None, help="IAM secret access key if user has a bucket."),
        s3_path: str = Option(None, help="Root-folder within bucket where the datasett should be copied."),
        generation_name: str = Option(None, help="Which generation to copy."),
        receipt_email: str = Option(None, help="Email address for progress notification."),
        debug: bool = Option(False, help="Print complete response to console"),
        endpoint: str = Option('', help="The endpoint to use for the API")
    ) -> None:
        """Initiates copying of a chosen generation of a datasett into a target bucket. If the user has no bucket, a temporary bucket with credentials is created."""
        response = self._bevaring().post(
            # temp url for local testing
            url='http://localhost:8000/bevaring/copy_dataset',
            json={
                'client_name': BEVARING_CLI_APP_NAME,
                'datasett_id': datasett_id,
                'user_has_bucket': user_has_bucket,
                'bucket_name': bucket_name,
                'iam_access_key_id': iam_access_key_id,
                'iam_secret_access_key': iam_secret_access_key,
                's3_path': s3_path,
                'generation_name': generation_name,
                'receipt_email': receipt_email
            }
        )

        ensure_success(response)
        json = response.json()

        if 'bucket_name' in json:
            copy_file_dict = toml.load(COPY_FILE)
            existing_ids = list(copy_file_dict.keys())
            copy_credentials_id = self.get_new_credentials_id(id, existing_ids)
            new_copy_credentials_dict = self.format_new_copy_credentials_dict(copy_credentials_id, json)
            copy_file_dict.update(new_copy_credentials_dict)

            with open(COPY_FILE, 'w') as f:
                toml.dump(copy_file_dict, f)

            if receipt_email:
                logger.info(f"Copying of datasett to bucket {json['bucket_name']} initiated. Await email notification.")
            else:
                logger.info(f"Copying of datasett to bucket {json['bucket_name']} initiated.")

    def aws(
        self,
        id: str = Argument(..., help="Id of the aws credentials to print."),
        debug: bool = Option(False, help="Print complete response to console")
    ) -> None:
        try:
            copy_credentials_dict = toml.load(COPY_FILE)[id]
            aws_export(copy_credentials_dict['iam_access_key_id'], copy_credentials_dict['iam_secret_access_key'])
        except Exception:
            print("The id was not found.")

    @staticmethod
    def get_new_credentials_id(id: str, existing_ids: List[str]):
        if id:
            if id not in existing_ids:
                copy_credentials_id = id
            else:
                raise Exception("The chosen id already exists.")
        else:
            current_highest_index = 0
            for id in existing_ids:
                if id.isdigit() and int(id) > current_highest_index:
                    current_highest_index = int(id)
            copy_credentials_id = str(current_highest_index + 1)
        return copy_credentials_id

    @staticmethod
    def format_new_copy_credentials_dict(copy_credentials_id: str, json: Any):
        new_copy_credentials_dict = {
                copy_credentials_id: {
                    'target_s3_uri': json['target_s3_uri'],
                    'iam_access_key_id': json['iam_access_key_id'],
                    'iam_secret_access_key': json['iam_secret_access_key'],
                    'expiry_date': 'Not yet implemented'
                }
            }
        return new_copy_credentials_dict
