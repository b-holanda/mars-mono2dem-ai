from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path
import re

from bridges.http import Http
from utils.logger import get_logger

logger = get_logger(__name__)

DEM_PATTERN = r"\.IMG$"
IS_FILE_PAT = r"\.[A-Za-z0-9]{1,5}$"

@dataclass(frozen=True)
class HiRISEConfig:
    samples: int
    http: Http

@dataclass
class HiRISENode:
    link: str
    loaded: bool = False
    child: List['HiRISENode'] = field(default_factory=list)

class HiRISEResolver:
    def __init__(self, root: str, http: Http):
        self.http = http
        self.dem_pattern = re.compile(DEM_PATTERN, re.I)
        self.is_file_pattern = re.compile(IS_FILE_PAT)
        self.source_suffix = "_RED.JP2"

        root = root.rstrip("/")
        self.dem_stack: List[HiRISENode] = []
        self.source_root = f"{root}/RDR"
        self._seen_dem_keys: set[str] = set()

        # >>> NOVO: pool de nós (cache por link)
        self._node_pool: dict[str, HiRISENode] = {}
        self.dem_stack.append(self._get_node(f"{root}/DTM/ESP/"))

    # ---------- utils ----------
    def _get_node(self, link: str) -> HiRISENode:
        """Retorna sempre o MESMO objeto HiRISENode para um link."""
        node = self._node_pool.get(link)
        if node is None:
            node = HiRISENode(link=link)
            self._node_pool[link] = node
        return node

    def _is_dem(self, link: str) -> bool:
        return bool(self.dem_pattern.search(link))

    def _is_file(self, link: str) -> bool:
        return bool(self.is_file_pattern.search(link))

    def _dem_key(self, link: str) -> str:
        return Path(urlparse(link).path).stem.lower()

    # ---------- core ----------
    def find_next(self) -> Optional[Tuple[str, str]]:
        while self.dem_stack:
            top = self.dem_stack[-1]
            logger.info(f"Looking inside: {top.link}")

            if self._is_dem(top.link):
                key = self._dem_key(top.link)
                if key in self._seen_dem_keys:
                    logger.info(f"Duplicate DEM skipped: {top.link}")
                    self.dem_stack.pop()
                    continue

                self._seen_dem_keys.add(key)
                dem_url = top.link
                source_url = self.compute_source_path(dem_url)

                # >>> NOVO: avance a pilha AGORA para não revisitar este .IMG
                self.dem_stack.pop()
                return dem_url, source_url

            # desce se já tem filhos
            if top.child:
                self.dem_stack.append(top.child.pop())
                continue

            # carrega filhos só uma vez por nó
            if not top.loaded and not self._is_file(top.link):
                logger.info(f"Loading children for: {top.link}")
                self._load_children_into_node(top)
                continue

            logger.info("Backtracking…")
            self.dem_stack.pop()

        return None

    # ---------- caching de filhos ----------
    def _load_children_into_node(self, node: HiRISENode) -> None:
        """Carrega e cacheia os filhos dentro do próprio nó (uma única vez)."""
        html_str = self.http.get(node.link)
        node.loaded = True  # marque já, mesmo que falhe, para não ficar em loop

        if not html_str:
            logger.info("Empty response.")
            node.child = []
            return

        soup = BeautifulSoup(html_str, "html.parser")
        children: List[HiRISENode] = []

        for a in soup.find_all("a"):
            href = (a.get("href") or "").strip()
            if not href or href in {"../", "./", "#"}:
                continue

            child_url = urljoin(node.link, href)

            # se aparenta ser diretório, normalize pra terminar com '/'
            if not self._is_file(child_url) and not child_url.endswith("/"):
                child_url += "/"

            # >>> use SEMPRE o pool para reusar nós
            children.append(self._get_node(child_url))
            logger.info(f" child -> {child_url}")

        # diretórios primeiro, depois arquivos, ambos ordenados por nome
        children.sort(key=lambda n: (self._is_file(n.link), n.link.lower()))
        node.child = children

    def compute_source_path(self, dem_url: str) -> str:
        dem_mono_pair = dem_url.split("/")[-2]
        dem_mono_pair_split = dem_mono_pair.split("_")
        orb = dem_url.split("/")[-3]
        monocular_left_observation = f"{dem_mono_pair_split[0]}_{dem_mono_pair_split[1]}_{dem_mono_pair_split[2]}"
        source_name = f"{monocular_left_observation}{self.source_suffix}"

        return f"{self.source_root}/{dem_mono_pair_split[0]}/{orb}/{monocular_left_observation}/{source_name}"

class HiRISEService:
    def __init__(self, config: HiRISEConfig):
        self.http = config.http
        self.samples = config.samples

    def download_samples(self):
        resolver = HiRISEResolver(root=self.http.host, http=self.http)

        while self.samples > 0:
            dem_url, source_url = resolver.find_next()

            base_dir = Path(__file__).resolve().parent.parent
            sample_dir = base_dir / "datasets" / "sources" / str(self.samples)
            sample_dir.mkdir(parents=True, exist_ok=True)

            dem_path = sample_dir / "DEM.IMG"
            mono_path = sample_dir / "MONO.JP2"

            logger.info(f"Downloading DEM samples: {dem_url}")

            self.http.download(url=dem_url, destination=str(dem_path))

            logger.info(f"Downloading source samples: {source_url}")

            self.http.download(url=source_url, destination=str(mono_path))

            self.samples -= 1
