from typing import List

class Script:
    def __init__(self, filename: str):
        self.script = self.getRawScript(filename)

    def getRawScript(self, filename: str) -> str:
        with open(filename, "r", encoding="utf-8") as script:
            return script.read()
    
    @staticmethod
    def getTabulation(line: str) -> int:
        return len(line) - len(line.lstrip(' '))

    def addData(self, placeholders: dict):
        splitedScript = self.script.splitlines()

        for i, line in enumerate(splitedScript):  # Usar enumerate para obtener el índice
            for holder, replacement in placeholders.items():
                # print(f"looking for {holder} in {line}")
                if holder in line:
                    # Reemplazar el contenido y actualizar splitedScript en el índice correspondiente
                    line = ' ' * self.getTabulation(line) + replacement
                    splitedScript[i] = line  # Actualizar la línea en splitedScript

        self.script = '\n'.join(splitedScript)