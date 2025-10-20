import sys
from rich.table import Table

from utils.logger import Logger
from utils.environment import config
from bridges.http import Http, HttpConfig
from services.HiRISE import HiRISEService, HiRISEConfig

console = Logger().console

def help():
    table = Table(title="Comandos disponíveis")

    table.add_column("Comando", justify="right", style="cyan", no_wrap=True)
    table.add_column("Descrição", style="magenta")

    table.add_row("load:sources", "Realizar o web scraping no repositório da HiRISE e monta os pares DEM/DTM com sua respectiva imagem Monocular")
    table.add_row("exit", "Fecha o modo interativo do CLI")

    console.print(table)

def load_sources():
    hirise_config = config().get("hirise")

    hirise_service = HiRISEService(
        config=HiRISEConfig(
            samples=hirise_config["samples"],
            http=Http(
                config=HttpConfig(
                    host=hirise_config["host"],
                )
            ),
        )
    )

    hirise_service.download_samples()

commands = {
    "load:sources": load_sources,
    "help": help,
}

def cli():
    setup_logging()

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
