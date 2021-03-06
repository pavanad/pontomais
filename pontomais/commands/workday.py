from pontomais.api.client import PontoMaisClient
from requests.exceptions import ProxyError

from .base import BaseCommand


class WorkdayCommand(BaseCommand):
    """
    Get information about the work day

    workday
        {day? : Put the workday (example: YYYY-MM-DD)}
    """

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
            day = self.argument("day")
            response = pontomais.work_day(day) if day else pontomais.current_work_day()
            if response.get("work_day") is None:
                self.line("No information found for that day.\n")
            else:
                self.__show_results(response)
            return

        self.line(
            "<error>Unable to log in to the API, check your credentials.</error>\n"
        )

    def __show_results(self, results: dict):

        workday = results["work_day"]
        time_cards = workday["time_cards"]
        if not len(time_cards):
            self.line("No information found for that day.\n")
            return

        self.line("All points of the day:")
        if len(time_cards) < 4:
            self.line("<error>Ops! Your records are incomplete.</error>")

        table = self.table()
        table.set_header_row(["Registro", "Recibo", "Horário"])

        rows = []
        for index, card in enumerate(time_cards):
            register = (
                "<fg=yellow>Entrada</>" if (index + 1) % 2 else "<fg=green>Saída</>"
            )
            rows.append([register, card["receipt"], card["time"]])

        table.set_rows(rows)
        table.render(self.io)
        self.line("")
