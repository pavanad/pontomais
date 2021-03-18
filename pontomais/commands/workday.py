from cleo import Command
from api.client import PontoMaisClient


class WorkdayCommand(Command):
    """
    Get information about the work day.

    workday
        {day? : Put the workday (example: YYYY-MM-DD)}
    """

    def handle(self):
        pontomais = PontoMaisClient()
        auth = pontomais.authenticate()
        if auth:
            day = self.argument("day")
            response = pontomais.work_day(day) if day else pontomais.current_work_day()
            print(response)

        self.line("\n<error>Unable to log in to the API, check your credentials.<error>")