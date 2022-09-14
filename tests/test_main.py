from typer.testing import CliRunner

from bevaring_cli.main import app

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert result.output == "bevaring-cli version 0.1.0\n"
