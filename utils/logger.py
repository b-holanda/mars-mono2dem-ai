from rich.console import Console

from utils.decorators import singleton

@singleton
class Logger:

    def __init__(self):
        self.console = Console()
