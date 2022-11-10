import logging

from bevaring_cli.exceptions import AuthenticationError

logger = logging.getLogger(__name__)

REAUTHENTICATE = " Please try to re-authenticate with: bevaring auth login"
COULD_NOT_AUTHENTICATE = "Could not authenticate." + REAUTHENTICATE
COULD_NOT_LOGIN = "Could not login." + REAUTHENTICATE


class Authentication:

    def get_credentials(self) -> dict:
        raise NotImplementedError("Not yet implemented")

    def logout(self) -> None:
        raise NotImplementedError("Not yet implemented")

    def login_with_device_code(self) -> dict:
        raise NotImplementedError("Not yet implemented")

    def login_interactive(self) -> dict:
        raise NotImplementedError("Not yet implemented")

    @staticmethod
    def validate_result(result) -> dict:
        if not result:
            raise AuthenticationError(COULD_NOT_LOGIN, 10)

        if "error" in result:
            logger.error(result)
            raise AuthenticationError(COULD_NOT_AUTHENTICATE, 11)

        if "id_token_claims" in result:
            id_token = result["id_token_claims"]
            return {
                **result,
                "username": id_token["preferred_username"],
                "tenant_id": id_token["tid"],
            }

        return result
