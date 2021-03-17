import os

CONFIG_FILENAME = "config"
CONFIG_ROOT_PATH = os.path.join(os.path.expanduser("~"), ".pontomais")


def config_path_exists() -> bool:
    return os.path.exists(CONFIG_ROOT_PATH)


def config_file_exists() -> bool:
    filename = os.path.join(CONFIG_ROOT_PATH, CONFIG_FILENAME)
    return os.path.exists(filename)