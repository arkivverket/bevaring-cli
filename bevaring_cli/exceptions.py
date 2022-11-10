from httpx import Response


class AuthenticationError(Exception):
    """Raised when authentication fails"""
    def __init__(self, message: str, exit_code: int):
        super().__init__(message)
        self.exit_code = exit_code


class ResponseError(Exception):
    def __init__(self, response: Response):
        super().__init__(f"{response.status_code} {response.reason_phrase} {response.text}")
        self.exit_code = response.status_code


def ensure_success(response: Response) -> None:
    if response and not response.is_success:
        raise ResponseError(response)
