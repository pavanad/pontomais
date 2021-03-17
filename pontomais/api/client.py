class PontoMaisClient:

    BASE_URL = "https://api.pontomais.com.br"

    def __init__(self) -> None:
        self.__username = None
        self.__password = None

    def set_credentials(self, username: str, password: str):
        self.__username = username
        self.__password = password
