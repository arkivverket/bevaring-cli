from typing import Dict

from functools import cache
from typer import get_app_dir
from rich.console import Console

from bevaring_cli import BEVARING_CLI_APP_NAME
from bevaring_cli.exceptions import AuthenticationError

# @TODO: replace this with production values
state: Dict[str, str | dict] = {
    "endpoint": "bevaring.dev.digitalarkivet.no",
    "credentials": {},
}

console = Console()


@cache
def get_config_directory() -> str:
    return get_app_dir(app_name=BEVARING_CLI_APP_NAME)


def validate_result(result) -> dict:
    if not result:
        console.print("[red]Could not login, an unknown error occured. Please try to re-authenticate:[/red]\nbevaring auth login")
        raise AuthenticationError()

    if "error" in result:
        console.print(result)
        console.print("[red]Could not authenticate, please re-authenticate with:[/red]\nbevaring auth login")
        raise AuthenticationError()

    if "id_token_claims" in result:
        id_token = result["id_token_claims"]
        return {
            **result,
            "username": id_token["preferred_username"],
            "tenant_id": id_token["tid"],
        }

    return result
