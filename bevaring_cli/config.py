from attrs import define
from bevaring_cli import BEVARING_CLI_APP_NAME
from click import get_app_dir
from enterprython import component, setting

CONFIG_DIR = get_app_dir(app_name=BEVARING_CLI_APP_NAME)
SESSION_FILE = f"{CONFIG_DIR}/session.toml"


@component()
@define(frozen=True, on_setattr=None)
class Config:
    client_id: str = setting('CLIENT_ID')  # do not use attribute path
    endpoint: str = setting('ENDPOINT')
    datasett_id: str = setting('DATASETT_ID')
    session_id: str = setting('SESSION_ID')
    bucket_name: str = setting('BUCKET_NAME')
    iam_access_key_id: str = setting('IAM_ACCESS_KEY_ID')
    iam_secret_access_key: str = setting('IAM_SECRET_ACCESS_KEY')
