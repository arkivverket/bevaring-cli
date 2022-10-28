import logging
import textwrap

from enterprython import component
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

log = logging.getLogger(__name__)


@component()
class DatasettCmd(Cmd):

    def __init__(self, app: App, bevaring: BevaringClient):
        super().__init__()
        self._bevaring = bevaring
        self.register(self.list, self.checkout, self.copy)
        app.add(self._app, 'datasett')

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
        response = self._bevaring().post(
            url='bevaring/checkout_dataset',
            json={
                'client_name': BEVARING_CLI_APP_NAME,
                'datasett_id': datasett_id,
                'with_data': not empty,
                'receipt_email': email
            }
        )

        response.raise_for_status()
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
        datasett_id: str = Argument(..., help="Identifier of the dataset to copy."),
        user_has_bucket: bool = Argument(False, help="If user has a target bucket to copy to."),
        bucket_name: str = Option('', help="Name of the target bucket."),
        iam_access_key_id: str = Option('', help="IAM acces key id if user has a bucket."),
        iam_secret_access_key: str = Option('', help="IAM secret access key if user has a bucket."),
        s3_path: str = Option('', help="Root-folder within bucket where the dataset should be copied."),
        s3_logfiles_path: str = Option('', help="Root-folder within bucket where logfiles should be stored."),
        generation_name: str = Option('', help="Which generation to copy."),
        receipt_email: str = Option('', help="Email address for progress notification."),
        debug: bool = Option(False, help="Print complete response to console"),
        endpoint: str = Option('', help="The endpoint to use for the API")
    ) -> None:
        """Initiates copying of a chosen generation of a dataset into a target bucket. If the user has no bucket, a temporary bucket with credentials is created."""
        response = self._bevaring().get(
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
                's3_logfiles_path': s3_logfiles_path,
                'generation_name': generation_name,
                'receipt_email': receipt_email
            }
        )

        response.raise_for_status()
        json = response.json()

        log.info(json)

        #datasett_id: UUID = Field(description="Identifikator av datasettet i Bevaring som ble sjekket ut")
        #session_id: UUID = Field(description="Unik identifikator av sesjonen denne operasjonen har startet")
        #bucket_name: str = Field(description="Navn på midlertidig S3 Bucket som er tilgjengelig for videre arbeid")
        #iam_access_key_id: str = Field(description="IAM nøkkel for å gjøre operasjoner mot S3. Del av et par")
        #iam_secret_access_key: str = Field(description="Hemmelig IAM nøkkel for å gjøre operasjoner mot S3. Del av et par")
        #s3_path: str | None = Field(description="Rot-mappe innenfor Bucket for å legge arkivuttrekket - innholdet i Tar-filen")
        #s3_logfiles_path: str | None = Field(description="Rot-mappe innenfor Bucket for å legge logg-filene som Mottak har generert")

        # Finn en god måte å sjekke om ting gikk bra eller ikke
        if 'bucket_name' in json:
            Console().print("Copying of dataset initiated... Await email confirmation when the copying is complete.")
