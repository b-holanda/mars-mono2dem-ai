import argparse
import sys
import numpy as np
import rasterio as rio

from pathlib import Path
from rasterio.enums import Resampling
from rasterio.warp import reproject
from rasterio.shutil import copy as rio_copy
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from concurrent.futures import ProcessPoolExecutor, as_completed

from utils.logger import Logger

console = Logger().console

@dataclass(frozen=True)
class GdalConfig:
    resampling: str
    dem_nodata: float
    source_path: str
    samples: int
    max_workers: int
    driver: str
    compressor_dem: str
    compressor_mono: str
    blocksize: int
    wrap_mem_limit: int
    overview_method: str
    gdal_cache: int
    num_threads: str

class Gdal:
    def __init__(self, config: GdalConfig):
        self.resampling = config.resampling
        self.dem_nodata = config.dem_nodata
        self.samples = config.samples
        self.max_workers = config.max_workers
        self.driver = config.driver
        self.compressor_dem = config.compressor_dem
        self.compressor_mono = config.compressor_mono
        self.blocksize = config.blocksize
        self.wrap_mem_limit = config.wrap_mem_limit
        self.overview_method = config.overview_method
        self.gdal_cache = config.gdal_cache
        self.num_threads = config.num_threads

        base_dir = Path(__file__).resolve().parent.parent

        self.source_path = base_dir / config.source_path / "sources"

    def convert(self):
        console.print("[bold green]Convertendo e alinhando HiRISE [yellow]MONO.JP2 [bold green]e [yellow]DEM.IMG [bold green]para seus respectivos GeoTIFFs.")

        scenes = [self.source_path / str(i) for i in range(1, self.samples + 1)]
        args_list = [(scene,) for scene in scenes]
        successes = 0

        with rio.Env(
            GDAL_CACHEMAX=int(self.gdal_cache),
            NUM_THREADS=self.num_threads,
            GDAL_NUM_THREADS=self.num_threads,
        ):
            with console.status(f"[bold green]Convertendo e alinhando cenas") as status:
                with ProcessPoolExecutor(max_workers=self.max_workers) as ex:
                    futs = [ex.submit(self.process_scene, *args) for args in args_list]
                    for f in as_completed(futs):
                        scene, ok = f.result()
                        if ok:
                            successes += 1
                        console.print(f"[OK] {scene}" if ok else f"[WARN] {scene} not processed")

    def process_scene(self, scene):
        jp2 = scene / "MONO.JP2"
        dem_img = scene / "DEM.IMG"

        if not jp2.exists() or not dem_img.exists():
            console.print(f"[yellow]SKIP[/] {scene} (missing MONO.JP2 or DEM.IMG)")
            return scene, False

        converted_dir = scene / "converted"

        converted_dir.mkdir(parents=True, exist_ok=True)

        mono_tif = converted_dir / "MONO.tif"
        dem_raw_tif = converted_dir / "DEM_raw.tif"
        dem_aligned_tif = converted_dir / "DEM_aligned.tif"

        if not mono_tif.exists():
            console.print("  → Converting MONO.JP2 → MONO.tif")
            self._convert_mono_jp2_to_tif(jp2, mono_tif)
        else:
            console.print("  ✓ MONO.tif already exists")

        if not dem_raw_tif.exists():
            console.print("  → Converting DEM.IMG → DEM_raw.tif")
            self._convert_dem_img_to_tif(dem_img, dem_raw_tif)
        else:
            console.print("  ✓ DEM_raw.tif already exists")

        console.print("  → Aligning DEM_raw.tif → DEM_aligned.tif (grid of MONO.tif)")
        self._align_dem_to_mono(dem_raw_tif, mono_tif, dem_aligned_tif)
        console.print("  ✓ Done\n")

        return scene, True

    def _convert_mono_jp2_to_tif(self, jp2: Path, mono_tif: Path):
        with rio.open(jp2) as source:
            rio_copy(
                source,
                mono_tif,
                driver=self.driver,
                copy_src_overviews=False,
                compress=self.compressor_mono,
                BIGTIFF="IF_SAFER",
                NUM_THREADS=self.num_threads,
                blocksize=self.blocksize,
                OVERVIEW_RESAMPLING=self.overview_method.upper()
            )

        return mono_tif

    def _convert_dem_img_to_tif(self, dem_img: Path, dem_raw_tif: Path):
        pass

    def _align_dem_to_mono(self, dem_img: Path, mono_tif: Path, dem_aligned_tif: Path):
        pass
