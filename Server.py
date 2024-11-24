from Script import Script
from DiscordLinks import DiscordLinks

from server_enums.Stadiums import Stadiums

from selenium.common.exceptions import TimeoutException

class Server:
    def __init__(self, filepath: str, hostName: str, adminPassword: str, stadium: Stadiums, gameTime: int, goalLimit: int, dsLinks: DiscordLinks = DiscordLinks()):
        self.script = Script(filepath)
        self.token = self.getToken()
        self.hostName = hostName
        self.adminPassword = adminPassword
        self.stadium = stadium
        self.gameTime = gameTime
        self.goalLimit = goalLimit
        self.dsLinks = dsLinks

    def getToken(self) -> str:
        with open("files/token.txt", "r") as token:
            return token.read().strip()

    def getScript(self) -> str:
        data = {
            "{{HOST_NAME}}": f"var NombreHost = \"{self.hostName}\";",
            "{{ADMIN_PASSWORD}}": f"var ClaveParaSerAdmin = \"{self.adminPassword}\";",
            "{{TOKEN}}": f"token: \"{self.getToken()}\",",
            "{{STADIUM}}": f"var MapaPorDefecto = \"{self.stadium.value}\";",
            "{{GAMETIME}}": f"var TiempoDeJuego = {self.gameTime};",
            "{{GOAL_LIMIT}}": f"var LimiteDeGoles = {self.goalLimit};",
            "{{DS_RECORDS_LINK}}": f"const GrabacionesDiscord = \"{self.dsLinks.server}\";",
            "{{DS_RECORDS_HOOK}}": f"const WebhookGrabaciones = \"{self.dsLinks.records}\";",
            "{{DS_KICKBANS}}": f"const AnuncioKicksBans = \"{self.dsLinks.kickBans}\";",
            "{{DS_SERVER_OPEN}}": f"var AnuncioHostAbierto = \"{self.dsLinks.hostOpen}\";",
            "{{DS_LINK}}": f"const DiscordLink = \"{self.dsLinks.server}\";",
            "{{DS_ADMIN_CALL}}": f"var WebhookParaLlamarAdmins = \"{self.dsLinks.adminCall}\";",
            "{{DS_HAXCHAT}}": f"var webhookMensajesJugadores = \"{self.dsLinks.haxChat}\";",
            "{{DS_ENTRYS}}": f"var webhookBoletero = \"{self.dsLinks.entrys}\";"
        }

        self.script.addData(data)
        
        return self.script.script
    
    # returns an empty string if the server has no open
    def getServerLink(self, wd) -> str:
        try:
            iFrame = wd.findElementByCSS(path="iframe[src*='30xIZB1N/__cache_static__/g/headless.html']")
            wd.switchToFrame(iFrame)
            LinkElement = wd.findElementByXPath(path="//a[contains(@href, 'https://www.haxball.com/play?c=')]")
            return LinkElement.get_attribute("href")
        except TimeoutException:
            return ""
