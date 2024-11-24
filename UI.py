from server_enums.OutputType import OutputType
import asyncio

from rich.console import Console
from rich.layout import Layout
from rich.text import Text
from rich.style import Style
from rich.prompt import Prompt

from datetime import datetime
import pytz

import sys
from time import sleep

DEFAULT_STYLE = Style(color="cyan", bold=False)

class UI:
    def __init__(self):
        self.console = Console()
        self.layout = Layout(name="root")
        
        self.inputText = ""
        self.messages = []

        self.inputCallback = None  # Callback para procesar comandos

    def setInputCallback(self, callback):
        # Se asigna el callback para procesar el input
        self.inputCallback = callback

    def create_layout(self):
        self.layout.split_row(
            Layout(name="topright", ratio=1),
            Layout(name="output", ratio=4),
        )

        self.layout["topright"].split_column(
            Layout(name="servers", ratio=4),
            Layout(name="status")
        )

    def toConsole(self, message: str, outType: OutputType, bold: bool):
        argentina_tz = pytz.timezone("America/Argentina/Buenos_Aires")
        current_time = datetime.now(argentina_tz).strftime("%H:%M:%S")

        label, color = outType.value
        time_display = Text(f"[{current_time}] ", style=Style(color="bright_yellow", bold=True))
        styledLabel = Text(f"{label}: ", style=Style(color=color, bold=bold))
        styledMessage = Text(f"{message}", style=Style(color=color))

        self.console.print(time_display + styledLabel + styledMessage)

    async def waitForInput(self):
        while True:
            userInput = await asyncio.to_thread(Prompt.ask, ">", default=self.inputText)
            if self.inputCallback:
                self.inputCallback(userInput)
            else:
                self.toConsole("No inputCallback available", outType=OutputType.ERROR, bold=True)

    async def run(self):
        try:
            while True:
                await self.waitForInput()

        except KeyboardInterrupt:
            self.inputCallback("stopserver")
            self.console.print("[bold red]Saliendo...[/bold red]")
            sleep(5)
            sys.exit(0)
