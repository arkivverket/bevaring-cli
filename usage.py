from bevaring_cli.main import app

"""
Helps typer cli generate usage document for bevaring. Might be used f.eks. with
typer usage utils docs --name bevaring --output USAGE.md
"""

app = app()._app
