from enum import Enum

class OutputType(Enum):
    USER = ("[USER]", "cyan")
    PROGRAM = ("[PROGRAM]", "blue")
    SERVER = ("[SERVER]", "white")
    ERROR = ("[ERROR]", "red")

    def __init__(self, label, color):
        self.label = label
        self.color = color