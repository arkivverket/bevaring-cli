import logging

from functools import cache
from typer import get_app_dir

from bevaring_cli import BEVARING_CLI_APP_NAME
from bevaring_cli.exceptions import AuthenticationError

# @TODO: replace this with production values
state = {
    "endpoint": "bevaring.dev.digitalarkivet.no",
    "credentials": None,
}


@cache
def get_config_directory() -> str:
    return get_app_dir(app_name=BEVARING_CLI_APP_NAME)


def validate_result(result) -> dict | None:
    if not result:
        print("[red]Could not login, an unknown error occured. Please try to re-authenticate:[/red]\nbevaring login")
        raise AuthenticationError()

    if "error" in result:
        logging.debug(result)
        print("[red]Could not authenticate, please re-authenticate with:[/red]\nbevaring login")
        raise AuthenticationError()

    if "id_token_claims" in result:
        id_token = result["id_token_claims"]
        return {
            **result,
            "username": id_token["preferred_username"],
            "tenant_id": id_token["tid"],
        }

    return result
