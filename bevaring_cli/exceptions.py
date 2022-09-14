from typer import Exit


class AuthenticationError(Exit):
    """Raised when authentication fails"""

    def __init__(self, code: int = 1) -> None:
        super().__init__(code)
