import logging
from textwrap import dedent
from typing import Any

from attrs import define
from enterprython import component, setting
from httpx import Response
from rich.console import Console
from rich.table import Table
from toml import dump
from typer import Argument, Option

from bevaring_cli import BEVARING_CLI_APP_NAME
from bevaring_cli.bevaring_client import BevaringClient
from bevaring_cli.commands.app import App
from bevaring_cli.commands.cmd import Cmd
from bevaring_cli.config import SESSION_FILE
from bevaring_cli.exceptions import ensure_success

logger = logging.getLogger(__name__)


@component(singleton=False)
@define(slots=False)
class SessionCmd(Cmd):

    _main: App
    _bevaring: BevaringClient
    datasett_id: str = setting('DATASETT_ID')
    session_id: str = setting('SESSION_ID')
    bucket_name: str = setting('BUCKET_NAME')
    iam_access_key_id: str = setting('IAM_ACCESS_KEY_ID')
    iam_secret_access_key: str = setting('IAM_SECRET_ACCESS_KEY')

    def __attrs_post_init__(self):
        super().__init__()
        self.register(self.checkout, self.aws)
        self._main.add(self._app, name='session', help="Manages process of new generation creation")

    def checkout(
        self,
        datasett_id: str = Argument(..., help="Identifier of the dataset to check out"),
        email: str = Argument(..., help="Email address where to send progress notification"),
        empty: bool = Option(True, help="If true check out empty bucket"),
        debug: bool = Option(False, help="Print complete response to console"),
        endpoint: str = Option('', help="The endpoint to use for the API")
    ) -> None:
        """Checks out given dataset into by default empty bucket. Response will be persisted for later use."""
        response = self.request_checkout(datasett_id, email, empty)
        ensure_success(response)
        json = response.json()
        self.persist(json)
        if debug:
            self.print(json)
        logger.info(f"Creation of the {json['bucket_name']} was triggered. Await email notification.")

    def aws(self) -> None:
        """Prints (but not logs) environment variables for use with aws cli."""
        if not self.session_id:
            raise Exception("You do not have an opened session. Please checkout first.")
        self.aws_export(self.iam_access_key_id, self.iam_secret_access_key)

    def request_checkout(self, datasett_id: str, email: str, empty: bool) -> Response:
        if self.session_id:
            raise Exception(f"You have an opened session ({self.session_id}). Please close it first.")
        return self._bevaring().post(
            url='bevaring/checkout_dataset',
            json={
                'client_name': BEVARING_CLI_APP_NAME,
                'datasett_id': datasett_id,
                'with_data': not empty,
                'receipt_email': email
            }
        )

    @staticmethod
    def print(json: Any) -> None:
        table = Table("Datasett ID", "Session ID", "Bucket Name", "IAM Key", "IAM Secret")
        table.add_row(
            json['datasett_id'],
            json['session_id'],
            json['bucket_name'],
            json['iam_access_key_id'],
            json['iam_secret_access_key'],
        )
        Console().print(table)

    @staticmethod
    def persist(json: Any) -> None:
        with open(SESSION_FILE, 'w') as f:
            dump(json, f)

    @staticmethod
    def aws_export(key: str, secret: str) -> None:
        Console().print(dedent(f"""
            alias awsb='aws --endpoint-url https://s3-oslo.arkivverket.no'
            export AWS_REGION=oslo
            export AWS_ACCESS_KEY_ID={key}
            export AWS_SECRET_ACCESS_KEY={secret}
        """))
