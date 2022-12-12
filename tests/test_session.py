import re

from os import path, remove
from pytest_httpx import HTTPXMock
from toml import load
from typer.testing import CliRunner

from bevaring_cli.config import SESSION_FILE
from bevaring_cli.main import app
from tests.auth_mock import AuthMock  # noqa: F401

runner = CliRunner()

expected_session = {
    'datasett_id': 'di',
    'session_id': 'si',
    'bucket_name': 'bn',
    'iam_access_key_id': 'ik',
    'iam_secret_access_key': 'is',
}

expected_creds = """
alias awsb='aws --endpoint-url https://s3-oslo.arkivverket.no'
export AWS_REGION=oslo
export AWS_ACCESS_KEY_ID=ik
export AWS_SECRET_ACCESS_KEY=is

"""


def setup_function():
    assert not path.exists(SESSION_FILE), f"Session file exists: {SESSION_FILE}. Please move it to another place."


def teardown_function():
    if path.exists(SESSION_FILE):
        remove(SESSION_FILE)


def test_checkout_saves_session(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method='POST',
        url=re.compile('^.*bevaring/checkout_dataset.*$'),
        json=expected_session,
    )
    result = runner.invoke(app('test')._app, ["session", "checkout", "123", "test@test"])

    assert result.exit_code == 0
    actual = load(SESSION_FILE)
    assert expected_session == actual


def test_aws_credentials_are_printed(httpx_mock: HTTPXMock):
    test_checkout_saves_session(httpx_mock)
    result = runner.invoke(app('test')._app, ["session", "aws"])
    assert result.exit_code == 0
    assert result.stdout == expected_creds


def test_authorization_headers_are_added(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method='POST',
        url=re.compile('^.*bevaring/checkout_dataset.*$'),
        json=expected_session,
        match_headers={'Authorization': "Bearer test"},
    )
    result = runner.invoke(app('test')._app, ["session", "checkout", "123", "test@test"])

    assert result.exit_code == 0
