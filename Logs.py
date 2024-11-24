import datetime
from UI import UI
from server_enums.OutputType import OutputType

class Logs:
    def __init__(self, date: datetime, ui: UI):
        self.date = date
        self.ui = ui        
        self.filename = self.getFilename()

    def getFilename(self) -> str:
        return self.date.strftime("%Y-%m-%d_%H-%M-%S.log")

    def addLog(self, message: str, outType: OutputType):
        filepath = "logs/" + self.filename
        
        toLog = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ": " + message + "\n"
        
        with open(filepath, "a", encoding='utf-8') as logfile:
            logfile.write(toLog)
        self.ui.toConsole(message, outType, False)