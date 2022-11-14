from enterprython import component

from bevaring_cli.auth import Authentication


@component()
class AuthMock(Authentication):

    def get_credentials(self) -> dict:
        return {'access_token': 'test'}
