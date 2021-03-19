import os

from .base import BaseCommand
from config import settings


class ConfigureCommand(BaseCommand):
    name = "configure"
    description = (
        "This command set up API credentials and the address used in the pontomais."
    )

    def __create_question(self, text, validator):
        question = self.create_question(text)
        question.set_validator(validator)
        return self.ask(question)

    def handle(self):
        # create case not exists
        if not settings.config_path_exists():
            os.mkdir(settings.CONFIG_ROOT_PATH)

        # user info
        self.line("")
        username = self.ask(f"{self.PREFIX}Pontomais username:")
        password = self.secret(f"{self.PREFIX}Pontomais password:")

        # address info
        self.line("")
        latitude = self.__create_question(
            f"{self.PREFIX}Latitude of the workplace:", float
        )
        longitude = self.__create_question(
            f"{self.PREFIX}Longitude of the workplace:", float
        )
        address = self.ask(f"{self.PREFIX}Address of where you are working:")

        filename = os.path.join(settings.CONFIG_ROOT_PATH, settings.CONFIG_FILENAME)
        with open(filename, "w") as config_file:
            config_file.write("[user]\n")
            config_file.write(f"username = {username}\n")
            config_file.write(f"password = {password}\n\n")
            config_file.write("[location]\n")
            config_file.write(f"latitude = {latitude}\n")
            config_file.write(f"longitude = {longitude}\n")
            config_file.write(f"address = {address}\n")
