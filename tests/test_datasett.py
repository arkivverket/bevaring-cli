import re

from pytest_httpx import HTTPXMock
from toml import load
from typer.testing import CliRunner

from bevaring_cli.config import SESSION_FILE
from bevaring_cli.main import app
from tests.auth_mock import AuthMock

runner = CliRunner()

expected = {
    'datasett_id': 'di',
    'session_id': 'si',
    'bucket_name': 'bn',
    'iam_access_key_id': 'ik',
    'iam_secret_access_key': 'is'
}


def test_checkout_saves_session(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method='POST',
        url=re.compile('^.*bevaring/checkout_dataset.*$'),
        json=expected
    )
    result = runner.invoke(app('test')._app, ["datasett", "checkout", "123", "test@test"])

    assert result.exit_code == 0
    actual = load(SESSION_FILE)
    assert expected == actual


def test_authorization_headers_are_added(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method='POST',
        url=re.compile('^.*bevaring/checkout_dataset.*$'),
        json=expected,
        match_headers={'Authorization': "Bearer test"}
    )
    result = runner.invoke(app('test')._app, ["datasett", "checkout", "123", "test@test"])

    assert result.exit_code == 0
