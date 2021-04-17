from .base import BaseCommand

from pontomais.config import settings


class ProxyCommand(BaseCommand):
    name = "proxy"
    description = "If you need to use a proxy, you can configure using this command"

    def handle(self):
        self.line("")
        if not settings.config_file_exists():
            self.line("<error>Configuration file not found</error>")
            self.line("Please use the command: <info>pontomais configure</info>")
            return

        http_proxy = self.ask(f"{self.PREFIX}HTTP proxy:", "")
        https_proxy = self.ask(f"{self.PREFIX}HTTPS proxy:", "")

        config = settings.get_configurations()
        config["proxy"] = {"http": http_proxy, "https": https_proxy}
        settings.set_configurations(config)
        self.line("")
