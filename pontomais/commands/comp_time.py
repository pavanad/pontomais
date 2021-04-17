from pontomais.api.client import PontoMaisClient
from requests.exceptions import ProxyError

from .base import BaseCommand


class CompTimeCommand(BaseCommand):
    name = "comp_time"
    description = "Get information about comp time"

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
            response = pontomais.get_comp_time()
            print(response)
            return

        self.line(
            "<error>Unable to log in to the API, check your credentials.</error>\n"
        )
