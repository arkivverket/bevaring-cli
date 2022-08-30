import pytest

from bevaring_cli.auth import Authentication
from bevaring_cli.utils import state


def test_auth():
    auth = Authentication()

    assert auth._msal_app_instance is None
    assert auth.client_id == "d18685f9-148d-4e9a-98b3-194bcd01bc95"
    assert auth.authority == "https://login.microsoftonline.com/99d3d298-60cf-4636-9772-4a191b6f0d94"
    assert auth.scopes == ["https://bevaring.dev.digitalarkivet.no/User.Login"]

    assert auth._msal_app_kwargs["authority"] == "https://login.microsoftonline.com/99d3d298-60cf-4636-9772-4a191b6f0d94"
    assert auth._msal_app_kwargs["app_name"] == "bevaring-cli"
    assert auth._msal_app_kwargs["app_version"] == "0.1.0"


def test_scope_builder():
    original_endpoint = state["endpoint"]
    assert Authentication()._scope_builder("User.Login") == "https://bevaring.dev.digitalarkivet.no/User.Login"

    state["endpoint"] = "login.microsoftonline.com"
    assert Authentication()._scope_builder(".default") == "https://login.microsoftonline.com/.default"

    state["endpoint"] = original_endpoint


def test_missing_scope():
    with pytest.raises(ValueError) as excinfo:
        Authentication()._scope_builder("")

    assert excinfo.value.args[0] == "Scope name is required"
