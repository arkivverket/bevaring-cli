import logging
from typing import List

from enterprython import component, assemble

from bevaring_cli import __version__
from bevaring_cli.Cmd import Cmd
from bevaring_cli.utils import console

logging.basicConfig(level=logging.INFO)  # Enable DEBUG log for entire script
logging.getLogger("msal").setLevel(logging.WARNING)  # Optionally disable MSAL DEBUG logs
logger = logging.getLogger(__name__)


@component()
class App(Cmd):
    def __init__(self):
        super().__init__()
        self.register(self.version)

    @staticmethod
    def version() -> None:
        """Prints the version"""
        console.print(f"bevaring-cli version {__version__}")


# @app.callback()
# def main(
#     endpoint: str = Option(
#         state["endpoint"],
#         help="The endpoint to use for the API",
#     ),
# ) -> None:
#     if endpoint:
#         """
#         Only inform the user if the endpoint is different from the default
#         stdout.isatty() is used to check if the output is a terminal or not, to avoid printing the message when piping the output to another command
#         """
#         if state["endpoint"] != endpoint and stdout.isatty():
#             console.print(f"Setting endpoint to [green]{endpoint}[/green]")
#         state["endpoint"] = endpoint
#

def all_cmds(cmds: List[Cmd]) -> Cmd:
    for cmd in cmds:
        if type(cmd) == App:
            return cmd


if __name__ == "__main__":
    from bevaring_cli.commands import *
    assemble(all_cmds).run()
