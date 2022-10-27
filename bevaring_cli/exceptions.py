from httpx import Response


class AuthenticationError(Exception):
    """Raised when authentication fails"""
    pass


class ResponseError(Exception):
    def __init__(self, response: Response):
        super().__init__(f"{response.status_code} {response.reason_phrase} {response.text}")


def ensure_success(response: Response) -> None:
    if response and not response.is_success:
        raise ResponseError(response)
