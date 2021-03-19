from .base import BaseCommand
from api.client import PontoMaisClient


class WorkdayCommand(BaseCommand):
    """
    Get information about the work day.

    workday
        {day? : Put the workday (example: YYYY-MM-DD)}
    """

    def handle(self):
        self.line("")
        pontomais = PontoMaisClient()
        auth = pontomais.authenticate()
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
        self.line("")
        self.line("All points of the day.\n")

        table = self.table()
        table.set_header_row(["Registro", "Recibo", "Horário"])

        rows = []
        workday = results["work_day"]
        for index, card in enumerate(workday["time_cards"]):
            register = (
                "<fg=yellow>Entrada</>" if (index + 1) % 2 else "<fg=green>Saída</>"
            )
            rows.append([register, card["receipt"], card["time"]])

        table.set_rows(rows)
        table.render(self.io)

        self.line("")
        if len(workday["time_cards"]) < 4:
            self.line("<error>Ops! Your records are incomplete.</error>\n")
