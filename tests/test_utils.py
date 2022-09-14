import pytest

from bevaring_cli.exceptions import AuthenticationError
from bevaring_cli.utils import validate_result


def test_none_result():
    with pytest.raises(AuthenticationError) as excinfo:
        validate_result(None)

    assert excinfo.value.exit_code == 1


def test_error_result(error_result):
    with pytest.raises(AuthenticationError) as excinfo:
        validate_result(error_result)

    assert excinfo.value.exit_code == 1


def test_valid_login_result(login_result):
    result = validate_result(login_result)

    assert result["token_type"] == "Bearer"
    assert result["access_token"] == login_result["access_token"]
    assert result["username"] == "AbeLi@microsoft.com"
    assert result["tenant_id"] == "9122040d-6c67-4c5b-b112-36a304b66dad"


def test_valid_refresh_result(refresh_result):
    result = validate_result(refresh_result)

    assert result["token_type"] == "Bearer"
    assert result["access_token"] == refresh_result["access_token"]
    assert "username" not in result
    assert "tenant_id" not in result
