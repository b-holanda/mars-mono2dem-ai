from dataclasses import dataclass
from requests import Session
from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, TotalFileSizeColumn, DownloadColumn
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
from typing import Any

from utils.logger import Logger

console = Logger().console

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

        response = session.get(url)
        response.raise_for_status()

        return response.content

    def download(self, url: str, destination: str, console: Console):
        session = _make_session()
        response = session.head(url)

        response.raise_for_status()

        content_length = float(response.headers.get('Content-Length') or 0)
        chunk_size = 128000
        step = (100*chunk_size)/content_length

        stream = session.get(url, stream=True)

        progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            DownloadColumn(),
            console=console
        )

        progress.start()

        task = progress.add_task(f"[red]Baixando {url.split("/")[-1]}", total=content_length)

        try:
            with open(destination, 'wb') as fd:
                for chunk in stream.iter_content(chunk_size=chunk_size):
                    fd.write(chunk)
                    progress.update(task, advance=chunk_size)
        except Exception as e:
            raise e
        finally:
            progress.stop()
