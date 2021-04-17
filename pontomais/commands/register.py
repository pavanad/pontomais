from pontomais.api.client import PontoMaisClient
from requests.exceptions import ProxyError

from .base import BaseCommand


class RegisterCommand(BaseCommand):
    """
    Register on time card

    register
        {--y|yes : Automatic yes to prompts}
    """

    name = "register"
    description = "Register on time card"

    def handle(self):
        self.line("")

        try:
            pontomais = PontoMaisClient()
            auth = pontomais.authenticate()
        except ProxyError as error:
            self.line("<error>Failed to establish a new connection</error>")
            self.line("Please try use the command: <info>pontomais proxy</info>\n")
            return
        except Exception as error:
            self.line(f"<error>{error}</error>\n")
            return

        if auth:
            confirmed = (
                self.option("yes")
                if self.option("yes")
                else self.confirm(f"{self.PREFIX}Continue with this action?", False)
            )
            if confirmed:
                response = pontomais.register()
                if "success" in response:
                    self.line("<info>Successfully registered</info>")
                    self.line(f"Your ip: {response['meta']['ip']}")
                    self.line(f"Your receipt: {response['receipt']}\n")
            return

        self.line(
            "<error>Unable to log in to the API, check your credentials.</error>\n"
        )
