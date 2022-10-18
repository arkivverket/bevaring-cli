import logging

from bevaring_cli import BEVARING_CLI_APP_NAME

log = logging.getLogger(__name__)

REAUTHENTICATE = " Please try to re-authenticate with: " + BEVARING_CLI_APP_NAME + " auth login"
COULD_NOT_AUTHENTICATE = "Could not authenticate." + REAUTHENTICATE
COULD_NOT_LOGIN = "Could not login." + REAUTHENTICATE


class Authentication:

    def get_credentials(self) -> dict:
        raise NotImplementedError("Not yet implemented")

