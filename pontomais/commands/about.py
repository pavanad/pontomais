from cleo import Command
from pyfiglet import Figlet


class AboutCommand(Command):
    name = "about"

    description = "Shows information about pontomais cli."

    def handle(self):
        custom_fig = Figlet(font="big")
        title = custom_fig.renderText("pontomais cli")
        self.line(
        f"""{title}\n<info>Essa ferramenta foi desenvolvida para facilitar a utilização do app pontomais.</info>
            """
        )