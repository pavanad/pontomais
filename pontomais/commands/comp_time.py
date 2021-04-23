from datetime import datetime, timedelta

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
            if response.get("time_balance") is None:
                self.line("No information found for comp time.\n")
            else:
                tb_seconds = int(response["time_balance"])
                time_balance = str(timedelta(seconds=abs(tb_seconds)))
                color = "<fg=green>" if tb_seconds >= 0 else "<fg=red>-"

                updated_at = datetime.fromisoformat(response["updated_at"])
                self.line(f"Comp time: {color}{time_balance}</>")
                self.line(f"Last updated: {updated_at.strftime('%d/%m/%Y')}\n")
            return

        self.line(
            "<error>Unable to log in to the API, check your credentials.</error>\n"
        )
