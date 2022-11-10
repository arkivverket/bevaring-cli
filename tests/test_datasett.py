import os
from os import path
from os.path import expanduser
import re

from pytest_httpx import HTTPXMock
from toml import load
from typer.testing import CliRunner

from bevaring_cli.config import SESSION_FILE, CREDENTIALS_FILE
from bevaring_cli.main import app
from tests.auth_mock import AuthMock  # noqa: F401

runner = CliRunner()

expected_session = {
    'datasett_id': 'di',
    'session_id': 'si',
    'bucket_name': 'bn',
    'iam_access_key_id': 'ik',
    'iam_secret_access_key': 'is'
}

expected_creds = """
[default]
aws_secret_access_key = ik
aws_access_key_id = is
"""

# TODO create test strings
# Consider pytest.fixture
expected_copy_creds = """

"""

expected_copy_creds_user_has_bucket = """

"""


def setup_function(function):
    assert not path.exists(SESSION_FILE), f"Session file exists: {SESSION_FILE}. Please move it to another place."


def teardown_function(function):
    if path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)


def test_checkout_saves_session(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method='POST',
        url=re.compile('^.*bevaring/checkout_dataset.*$'),
        json=expected_session
    )
    result = runner.invoke(app('test')._app, ["datasett", "checkout", "123", "test@test"])

    assert result.exit_code == 0
    actual = load(SESSION_FILE)
    assert expected_session == actual


def test_checkout_saves_aws_credentials(httpx_mock: HTTPXMock):
    test_checkout_saves_session(httpx_mock)
    with open(expanduser(CREDENTIALS_FILE)) as f:
        assert expected_creds == f.read()


def test_authorization_headers_are_added(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method='POST',
        url=re.compile('^.*bevaring/checkout_dataset.*$'),
        json=expected_session,
        match_headers={'Authorization': "Bearer test"}
    )
    result = runner.invoke(app('test')._app, ["datasett", "checkout", "123", "test@test"])

    assert result.exit_code == 0


# TODO tests
def test_copy_saves_credentials(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method='POST',
        url=re.compile('^.*bevaring/copy_dataset.*$'),
        json=expected_session
    )

    result = runner.invoke(app('test')._app, ["datasett", "copy", "123"])

    print(result)

    assert result.exit_code == 0

# test_copy_saves_credentials_no_bucket
# test_copy_saves_credentials_user_has_bucket
# test_list_copies
# test index
# test alias/id
# test Exception existing id
