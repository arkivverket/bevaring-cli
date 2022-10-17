from logging import INFO

from typer.testing import CliRunner

from bevaring_cli.commands.app import VERSION
from bevaring_cli.main import app

runner = CliRunner()


def test_version(caplog):
    caplog.set_level(INFO)
    result = runner.invoke(app()._app, ["version"])
    assert result.exit_code == 0
    assert len(caplog.messages) == 1
    assert caplog.messages[0] == VERSION
