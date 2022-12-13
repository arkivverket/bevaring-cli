import pytest
from enterprython import assemble
from enterprython._inject import ENTERPRYTHON_COMPONENTS, load_config

from bevaring_cli.auth import Authentication, COULD_NOT_LOGIN, COULD_NOT_AUTHENTICATE
from bevaring_cli.auth_prod import AuthenticationProd
from bevaring_cli.exceptions import AuthenticationError


def auth_prod() -> AuthenticationProd:
    load_config(app_name='test', paths=['bevaring_cli/app.toml'])
    auth = assemble(AuthenticationProd)
    # Remove Prod version from container such that it will not conflict with the mock used in other tests.
    # This is only needed due to bug in Enterprython where profiles are not working correctly.
    ENTERPRYTHON_COMPONENTS.remove(next(a for a in ENTERPRYTHON_COMPONENTS if a.get_instance() == auth))
    return auth


def test_auth():
    auth = auth_prod()

    assert auth._msal_app_instance is None
    assert auth.authority == "https://login.microsoftonline.com/organizations"
    assert auth.scopes == ["https://bevaring.digitalarkivet.no/User.Login"]

    assert auth._msal_app_kwargs["authority"] == "https://login.microsoftonline.com/organizations"
    assert auth._msal_app_kwargs["app_name"] == "bevaring-cli"
    assert auth._msal_app_kwargs["app_version"] == "0.3.0"


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
