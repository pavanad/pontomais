from pontomais.api.client import PontoMaisClient

from .base import BaseCommand


class RegisterCommand(BaseCommand):
    name = "register"
    description = "Register on time card"

    def handle(self):
        self.line("")
        pontomais = PontoMaisClient()
        auth = pontomais.authenticate()
        if auth:
            response = pontomais.register()
            print(response)
            return

        self.line(
            "<error>Unable to log in to the API, check your credentials.</error>\n"
        )
