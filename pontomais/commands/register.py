from pontomais.api.client import PontoMaisClient

from .base import BaseCommand


class RegisterCommand(BaseCommand):
    name = "register"
    description = "Register on time card"

    def handle(self):
        self.line("")

        try:
            pontomais = PontoMaisClient()
            auth = pontomais.authenticate()
        except Exception as error:
            self.line(f"<error>{error}</error>\n")
            return

        if auth:
            if self.confirm(f"{self.PREFIX}Continue with this action?", False):
                response = pontomais.register()
                if "success" in response:
                    self.line("<info>Successfully registered</info>")
                    self.line(f"Your ip: {response['meta']['ip']}")
                    self.line(f"Your receipt: {response['receipt']}\n")
            return

        self.line(
            "<error>Unable to log in to the API, check your credentials.</error>\n"
        )
