from cleo import Command


class BaseCommand(Command):

    PREFIX = "> <comment>[pontomais]</comment> "

    def line(self, text, style=None, verbosity=None):
        text = self.PREFIX + text if text else ""
        super().line(text, style, verbosity)
