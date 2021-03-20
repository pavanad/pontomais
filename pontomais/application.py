from cleo import Application as BaseApplication

from .commands.about import AboutCommand
from .commands.configure import ConfigureCommand
from .commands.workday import WorkdayCommand
from .commands.register import RegisterCommand
from .commands.proxy import ProxyCommand

try:
    from pontomais.__version__ import __version__
except ImportError:
    from __version__ import __version__


class Application(BaseApplication):
    def __init__(self):
        super(Application, self).__init__("pontomais", __version__)

        for command in self.get_default_commands():
            self.add(command)

    def get_default_commands(self) -> list:
        commands = [
            AboutCommand(),
            ConfigureCommand(),
            WorkdayCommand(),
            RegisterCommand(),
            ProxyCommand(),
        ]
        return commands
