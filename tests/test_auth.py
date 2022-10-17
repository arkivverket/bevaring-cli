import pytest

from bevaring_cli.auth import Authentication, REAUTHENTICATE, COULD_NOT_LOGIN, COULD_NOT_AUTHENTICATE
from bevaring_cli.exceptions import AuthenticationError
from enterprython import assemble

from bevaring_cli.main import app


def test_auth():
    app()
    auth = assemble(Authentication)

    assert auth._msal_app_instance is None
    assert auth.cfg.client_id == "d18685f9-148d-4e9a-98b3-194bcd01bc95"
    assert auth.authority == "https://login.microsoftonline.com/organizations"
    assert auth.scopes == ["https://bevaring.dev.digitalarkivet.no/User.Login"]

    assert auth._msal_app_kwargs["authority"] == "https://login.microsoftonline.com/organizations"
    assert auth._msal_app_kwargs["app_name"] == "bevaring-cli"
    assert auth._msal_app_kwargs["app_version"] == "0.1.0"


def test_none_result():
    with pytest.raises(AuthenticationError) as excinfo:
        Authentication.validate_result(None)

    assert str(excinfo.value) == COULD_NOT_LOGIN


def test_error_result(error_result):
    with pytest.raises(AuthenticationError) as excinfo:
        Authentication.validate_result(error_result)

    assert str(excinfo.value) == COULD_NOT_AUTHENTICATE


def test_valid_login_result(login_result):
    result = Authentication.validate_result(login_result)

    assert result["token_type"] == "Bearer"
    assert result["access_token"] == login_result["access_token"]
    assert result["username"] == "AbeLi@microsoft.com"
    assert result["tenant_id"] == "9122040d-6c67-4c5b-b112-36a304b66dad"


def test_valid_refresh_result(refresh_result):
    result = Authentication.validate_result(refresh_result)

    assert result["token_type"] == "Bearer"
    assert result["access_token"] == refresh_result["access_token"]
    assert "username" not in result
    assert "tenant_id" not in result
