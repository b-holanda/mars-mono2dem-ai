from dataclasses import dataclass
from requests import Session
from requests.exceptions import RequestException
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
from typing import Any

from utils.logger import get_logger

logger = get_logger(__name__)

@dataclass(frozen=True)
class HttpConfig:
    host: str


def _make_session():
    retry = Retry(total=4, backoff_factor=0.5,
                  status_forcelist=[429, 500, 502, 503, 504],
                  allowed_methods=None)

    s = Session()
    s.mount("https://", HTTPAdapter(max_retries=retry))
    s.headers.update({"User-Agent": "MONO2DEM_BOT/1.0"})

    return s

class Http:
    def __init__(self, config: HttpConfig):
        self.host = config.host

    def get(self, url: str) -> bytes | Any:
        session = _make_session()

        try:
            response = session.get(url)
            response.raise_for_status()

            return response.content
        except RequestException as e:
            logger.error(f"Failed request for razon: {e}")

    def download(self, url: str, destination: str):
        session = _make_session()

        try:
            response = session.get(url, stream=True)

            with open(destination, 'wb') as fd:
                for chunk in response.iter_content(chunk_size=128):
                    fd.write(chunk)

        except RequestException as e:
            logger.error(f"Failed request for razon: {e}")
