import os
from configparser import ConfigParser

CONFIG_FILENAME = "config"
CONFIG_ROOT_PATH = os.path.join(os.path.expanduser("~"), ".pontomais")


def config_path_exists() -> bool:
    return os.path.exists(CONFIG_ROOT_PATH)


def config_file_exists() -> bool:
    filename = os.path.join(CONFIG_ROOT_PATH, CONFIG_FILENAME)
    return os.path.exists(filename)


def get_configurations() -> ConfigParser:
    configuration = ConfigParser()
    configuration.read(os.path.join(CONFIG_ROOT_PATH, CONFIG_FILENAME))
    return configuration


def set_configurations(configuration: ConfigParser):
    filename = os.path.join(CONFIG_ROOT_PATH, CONFIG_FILENAME)
    with open(filename, "w") as config_file:
        configuration.write(config_file)
