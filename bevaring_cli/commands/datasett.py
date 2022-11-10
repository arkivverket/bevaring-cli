import logging
import textwrap
import toml

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
from bevaring_cli.config import SESSION_FILE, CREDENTIALS_FILE, COPY_FILE
from bevaring_cli.exceptions import ensure_success

log = logging.getLogger(__name__)


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
        self.register(self.list, self.checkout, self.copy, self.aws)
        self._main.add(self._app, 'datasett')

    def list(
        self,
        limit: int = Option(2, help="Max amount of datasetts to list"),
        copies: bool = Option(None, help="Lists all locally stored credentials from the copy operation"),
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

    def checkout(
        self,
        datasett_id: str = Argument(..., help="Identifier of the datasett to check out."),
        email: str = Argument(..., help="Email address where to send progress notification."),
        empty: bool = Option(True, help="If true check out empty bucket"),
        debug: bool = Option(False, help="Print complete response to console"),
        endpoint: str = Option('', help="The endpoint to use for the API")
    ) -> None:
        """Checks out given datasett into by default empty bucket. Response will be saved into hidden file."""

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
            log.info(f"Creation of the {json['bucket_name']} was triggered. Await email notification.")

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
            copy_dict = toml.load(COPY_FILE)
            existing_ids = []

            for key in copy_dict:
                existing_ids.append(key)

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

            new_copy_credentials_dict = {
                copy_credentials_id: {
                    'target_s3_uri': json['target_s3_uri'],
                    'iam_access_key_id': json['iam_access_key_id'],
                    'iam_secret_access_key': json['iam_secret_access_key'],
                    'expiry_date': 'Not yet implemented'
                }
            }
            copy_dict.update(new_copy_credentials_dict)

            with open(COPY_FILE, 'w') as f:
                toml.dump(copy_dict, f)

            if receipt_email:
                log.info(f"Copying of datasett to bucket {json['bucket_name']} initiated. Await email notification.")
            else:
                log.info(f"Copying of datasett to bucket {json['bucket_name']} initiated.")

    def aws(
        self,
        id: str = Argument(..., help="Id of the aws credentials to print."),
        debug: bool = Option(False, help="Print complete response to console")
    ) -> None:
        copy_dict = toml.load(COPY_FILE)


# Create command aws, tar inn id , leser iam_acces_key_id og iam_secret_access_key og sender disse til Pawel sin awsprint funksjon
