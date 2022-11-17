from os import path
import os
import re

from pytest_httpx import HTTPXMock
from typer.testing import CliRunner
from toml import load

from bevaring_cli.config import COPY_FILE
from bevaring_cli.main import app

runner = CliRunner()


def setup_function():
    assert not path.exists(COPY_FILE), f"Copy file exists: {COPY_FILE}. Please move it to another place."


def teardown_function():
    if path.exists(COPY_FILE):
        os.remove(COPY_FILE)


def test_copy_saves_credentials_as_expected(
    httpx_mock: HTTPXMock,
    copy_response,
    command_input_id,
    expected_creds
):
    httpx_mock.add_response(
        method='POST',
        url=re.compile('^.*bevaring/copy_dataset.*$'),
        json=copy_response
    )
    runner.invoke(app('test')._app, command_input_id)
    actual = load(COPY_FILE)['test1']

    assert actual == expected_creds


def test_copy_saves_credentials_with_s3_path_as_expected(
    httpx_mock: HTTPXMock,
    copy_response_with_s3_path,
    command_input_id_with_s3_path,
    expected_creds_with_s3_path
):
    httpx_mock.add_response(
        method='POST',
        url=re.compile('^.*bevaring/copy_dataset.*$'),
        json=copy_response_with_s3_path
    )
    runner.invoke(app('test')._app, command_input_id_with_s3_path)
    actual = load(COPY_FILE)['test2']

    assert actual == expected_creds_with_s3_path


def test_copy_saves_credentials_with_incremental_indexing_as_expected(
    httpx_mock: HTTPXMock,
    copy_response,
    command_input_index_increment_test
):
    httpx_mock.add_response(
        method='POST',
        url=re.compile('^.*bevaring/copy_dataset.*$'),
        json=copy_response
    )
    runner.invoke(app('test')._app, command_input_index_increment_test)
    runner.invoke(app('test')._app, command_input_index_increment_test)
    copy_file_dict = load(COPY_FILE)
    actual_ids = list(copy_file_dict.keys())

    expected_ids = ['1', '2']

    assert actual_ids == expected_ids


def test_list_copies_returns_output_as_expected(
    httpx_mock: HTTPXMock,
    copy_response,
    command_input,
    command_input_print_copies_file
):
    httpx_mock.add_response(
        method='POST',
        url=re.compile('^.*bevaring/copy_dataset.*$'),
        json=copy_response
    )

    runner.invoke(app('test')._app, command_input)
    actual = runner.invoke(app('test')._app, command_input_print_copies_file)

    expected = 'id: 1\ttarget_s3_uri: s3://bn/di/ip0\n'

    assert actual.output == expected


def test_list_copies_informs_user_when_no_copies_file_exists(command_input_print_copies_file):
    actual = runner.invoke(app('test')._app, command_input_print_copies_file)

    expected = 'No copy credentials file exists since no copies have been created yet.\n'

    assert actual.output == expected


def test_copy_raises_KeyError_when_id_already_exists(
    httpx_mock: HTTPXMock,
    copy_response,
    command_input_id
):
    httpx_mock.add_response(
        method='POST',
        url=re.compile('^.*bevaring/copy_dataset.*$'),
        json=copy_response
    )
    runner.invoke(app('test')._app, command_input_id)
    result = runner.invoke(app('test')._app, command_input_id)

    assert result.exception.__class__ == KeyError


def test_aws_export_prints_creds_as_expected(
    httpx_mock: HTTPXMock,
    copy_response,
    command_input_id,
    command_input_aws_export
):
    httpx_mock.add_response(
        method='POST',
        url=re.compile('^.*bevaring/copy_dataset.*$'),
        json=copy_response
    )
    runner.invoke(app('test')._app, command_input_id)
    actual = runner.invoke(app('test')._app, command_input_aws_export)

    expected = "\nalias awsb='aws --endpoint-url https://s3-oslo.arkivverket.no'\nexport AWS_REGION=oslo\nexport AWS_ACCESS_KEY_ID=ik\nexport AWS_SECRET_ACCESS_KEY=is\n\n"

    assert actual.output == expected


def test_aws_export_raises_KeyError_when_id_not_found(
    httpx_mock: HTTPXMock,
    copy_response,
    command_input_id,
    command_input_aws_export_id_not_found
):
    httpx_mock.add_response(
        method='POST',
        url=re.compile('^.*bevaring/copy_dataset.*$'),
        json=copy_response
    )
    runner.invoke(app('test')._app, command_input_id)
    result = runner.invoke(app('test')._app, command_input_aws_export_id_not_found)

    assert result.exception.__class__ == KeyError
