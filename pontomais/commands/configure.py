import os
from configparser import ConfigParser

from pontomais.config import settings

from .base import BaseCommand


class ConfigureCommand(BaseCommand):
    name = "configure"
    description = (
        "This command set up API credentials and the address used in the pontomais"
    )

    def __create_question(self, text, validator):
        question = self.create_question(text, default="")
        question.set_validator(validator)
        return self.ask(question)

    def handle(self):
        # create case not exists
        if not settings.config_path_exists():
            os.mkdir(settings.CONFIG_ROOT_PATH)

        # user info
        self.line("")
        username = self.ask(f"{self.PREFIX}Pontomais username:", "")
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
        self.line("")

        config = ConfigParser()
        config["user"] = {"username": username, "password": password}
        config["location"] = {
            "latitude": latitude,
            "longitude": longitude,
            "address": address,
        }
        settings.set_configurations(config)
