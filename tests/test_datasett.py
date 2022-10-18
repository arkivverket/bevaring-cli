import re

from typer.testing import CliRunner
from enterprython import component, assemble
from pytest_httpx import HTTPXMock

from bevaring_cli.auth import Authentication
from bevaring_cli.main import app

runner = CliRunner()


@component()
class AuthMock(Authentication):

    def get_credentials(self) -> dict:
        return {'access_token': 'test'}


def test_datasett(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method='POST',
        url=re.compile('^.*bevaring/checkout_dataset.*$'),
        json={
            'datasett_id': 'di',
            'session_id': 'si',
            'bucket_name': 'bn',
            'iam_access_key_id': 'ik',
            'iam_secret_access_key': 'is'
        }
    )
    result = runner.invoke(app('test')._app, ["datasett", "checkout", "123", "test@test"])

    assert result.exit_code == 0
