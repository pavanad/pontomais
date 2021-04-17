import datetime
import json
import uuid

import requests
from pontomais.config.settings import get_configurations


class PontoMaisClient:

    BASE_URL = "https://api.pontomais.com.br"

    def __init__(self, username: str = None, password: str = None) -> None:
        self.__username = username
        self.__password = password
        self.__uuid = str(uuid.uuid1())
        self.__session = requests.Session()

    def __get_auth_url(self) -> str:
        """Get auth url for authentication.

        Returns:
            str: authentication url.
        """
        return f"{self.BASE_URL}/api/auth/sign_in"

    def __get_configurations(self):
        """Get configurations from config files case exists."""

        config = get_configurations()
        if config.has_section("user"):
            self.__username = config.get("user", "username")
            self.__password = config.get("user", "password")

        if config.has_section("location"):
            self.__address = config.get("location", "address")
            self.__latitude = config.get("location", "latitude")
            self.__longitude = config.get("location", "longitude")

        if config.has_section("proxy"):
            self.__session.verify = False
            self.__session.proxies = {
                "http": config.get("proxy", "http"),
                "https": config.get("proxy", "https"),
            }

    def __get_header(self) -> dict:
        return {
            "Host": self.BASE_URL.replace("https://", ""),
            "Content-Type": "application/json;charset=utf-8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:86.0) Gecko/20100101 Firefox/86.0",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://app.pontomaisweb.com.br",
            "Referer": "https://app.pontomaisweb.com.br//",
            "uid": self.__username,
            "uuid": self.__uuid,
            "access-token": self.__token,
            "token-type": "Bearer",
            "expiry": self.__expiry,
            "Api-Version": "2",
            "client": self.__client,
            "content-type": "application/json",
        }

    def set_location(self, address: str, latitude: float, longitude: float):
        """Set address of where you are working.

        Args:
            address (str): address of where you are working.
            latitude (float): latitude of the workplace.
            longitude (float): longitude of the workplace.
        """
        self.__address = address
        self.__latitude = latitude
        self.__longitude = longitude

    def set_credentials(self, username: str, password: str):
        """Set credentials of the pontomais api.

        Args:
            username (str): pontomais username.
            password (str): pontomais password.
        """
        self.__username = username
        self.__password = password

    def authenticate(self) -> bool:
        """Authenticates to the api."""

        token = None
        client = None
        expiry = None
        authenticated = False

        # case not credentials try get configurations
        if not all([self.__username, self.__password]):
            self.__get_configurations()

        auth_url = self.__get_auth_url()
        credentials = {"login": self.__username, "password": self.__password}
        response = self.__session.post(auth_url, data=credentials)

        if response.content and response.status_code == 201:
            authenticated = True
            response_json = response.json()
            token = response_json.get("token")
            client = response_json.get("client_id")
            expiry = response_json.get("expiry")

        self.__token = token
        self.__client = client
        self.__expiry = expiry

        return authenticated

    def work_day(self, day: str) -> dict:
        """Get work day.

        Args:
            day (str): work day (example YYYY-MM-DD)

        Returns:
            dict: data of the work day
        """
        url = f"{self.BASE_URL}/api/time_card_control/current/work_days/{day}"
        response = self.__session.get(url, headers=self.__get_header())
        return response.json()

    def current_work_day(self) -> dict:
        """Get current work day.

        Returns:
            dict: data of the current day.
        """
        today = datetime.date.today()
        return self.work_day(str(today))

    def register(self) -> dict:
        """Punch the clock in pontomais.

        Returns:
            dict: data of the response.
        """
        url = f"{self.BASE_URL}/api/time_cards/register"
        payload = {
            "time_card": {
                "latitude": self.__latitude,
                "longitude": self.__longitude,
                "address": self.__address,
                "reference_id": None,
                "original_latitude": self.__latitude,
                "original_longitude": self.__longitude,
                "original_address": self.__address,
                "location_edited": True,
            },
            "_path": "/meu_ponto/registro_de_ponto",
            "_device": {
                "browser": {
                    "name": "Firefox",
                    "version": "86.0",
                    "versionSearchString": "Firefox",
                },
            },
            "_appVersion": "0.10.32",
        }
        response = self.__session.post(
            url, headers=self.__get_header(), data=json.dumps(payload)
        )
        return response.json()
