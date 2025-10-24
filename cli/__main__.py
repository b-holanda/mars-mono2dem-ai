import sys
from rich.table import Table

from utils.logger import Logger
from utils.environment import config
from bridges.http import Http, HttpConfig
from services.HiRISE import HiRISEService, HiRISEConfig
from services.Gdal import  Gdal, GdalConfig

console = Logger().console

def help():
    table = Table(title="Comandos disponíveis")

    table.add_column("Comando", justify="right", style="cyan", no_wrap=True)
    table.add_column("Descrição", style="magenta")

    table.add_row("load:sources", "Realizar o web scraping no repositório da HiRISE e monta os pares DEM/DTM com sua respectiva imagem Monocular")
    table.add_row("convert:sources", "Converte e alinha HiRISE MONO.JP2 e DEM.IMG para seus respectivos GeoTIFFs.")
    table.add_row("exit", "Fecha o modo interativo do CLI")

    console.print(table)

def load_sources():
    hirise_config = config().get("hirise") or {}

    hirise_service = HiRISEService(
        config=HiRISEConfig(
            samples=hirise_config.get("samples", 100),
            http=Http(
                config=HttpConfig(
                    host=hirise_config.get("host", "https://www.uahirise.org/PDS"),
                )
            ),
        )
    )

    hirise_service.download_samples()

def convert_sources():
    gdal_config_raw = config().get("gdal") or {}

    gdal_service = Gdal(
        config=GdalConfig(
            resampling=gdal_config_raw.get("resampling", "bilinear"),
            dem_nodata=gdal_config_raw.get("dem_nodata", -32767.0),
            source_path=gdal_config_raw.get("source_path", "datasets"),
            driver=gdal_config_raw.get("driver", "GTiff"),
            compressor_dem=gdal_config_raw.get("compressor_dem", "LZW"),
            compressor_mono=gdal_config_raw.get("compressor_mono", "LZW"),
            blocksize=gdal_config_raw.get("blocksize", 512),
            overview_method=gdal_config_raw.get("overview_method", "BILINEAR"),
            gdal_cache=gdal_config_raw.get("gdal_cache", 6144),
            predictor_dem=gdal_config_raw.get("predictor_dem", 2),
            num_threads=gdal_config_raw.get("num_threads", "ALL_CPUS"),
            samples= (config().get("hirise") or {}).get("samples", 100),

        )
    )

    gdal_service.convert()

commands = {
    "load:sources": load_sources,
    "convert:sources": convert_sources,
    "help": help,
}

def cli():
    command_raw = ""

    while command_raw != "exit":
        command_raw = console.input("[bold green]Mars Mono to Dem AI CLI v1.0, digite [cyan]help [bold green]para ver os comandos\n>>> ")

        if command_raw != "exit":
            try:
                commands[command_raw]()
            except Exception:
                console.print_exception(show_locals=True)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            commands[sys.argv[1]]()
        except Exception:
            console.print_exception(show_locals=True)
    else:
        cli()
