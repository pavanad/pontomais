import os

from cleo import Command


class ConfigureCommand(Command):
    name = "configure"
    description = (
        "This command set up API credentials and the address used in the pontomais."
    )

    CONFIG_FILENAME = "config"
    CONFIG_ROOT_PATH = os.path.join(os.path.expanduser("~"), ".pontomais")

    def __config_path_exists(self) -> bool:
        return os.path.exists(self.CONFIG_ROOT_PATH)

    def __create_question(self, text, validator):
        question = self.create_question(text)
        question.set_validator(validator)
        return self.ask(question)

    def handle(self):
        # create case not exists
        if not self.__config_path_exists():
            os.mkdir(self.CONFIG_ROOT_PATH)

        # user info
        self.line("")
        username = self.ask("Pontomais username:")
        password = self.secret("Pontomais password:")

        # address info
        self.line("")
        latitude = self.__create_question("Latitude of the workplace:", float)
        longitude = self.__create_question("Longitude of the workplace:", float)
        address = self.ask("Address of where you are working:")

        filename = os.path.join(self.CONFIG_ROOT_PATH, self.CONFIG_FILENAME)
        with open(filename, "w") as config_file:
            config_file.write("[user]\n")
            config_file.write(f"username = {username}\n")
            config_file.write(f"password = {password}\n\n")
            config_file.write("[location]\n")
            config_file.write(f"latitude = {latitude}\n")
            config_file.write(f"longitude = {longitude}\n")
            config_file.write(f"address = {address}\n")
