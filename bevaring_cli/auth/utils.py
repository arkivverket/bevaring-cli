import logging
from rich import print

from bevaring_cli.exceptions import AuthenticationError


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
            "username": id_token["preferred_username"],
            "tenant_id": id_token["tid"],
        }

    return None
