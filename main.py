from datetime import datetime
import asyncio

from Server import Server
from DiscordLinks import DiscordLinks
from Manager import Manager
from UI import UI
from Logs import Logs

from server_enums.Stadiums import Stadiums

discordLinks = DiscordLinks(
    server =    "discord.gg/2UXsPaHRHq",
    kickBans =  "https://discord.com/api/webhooks/1297254030535295026/NPjKlluTgQFjfIuhm1n8B-j8G-kQLuES7fchx2b-TLRMED7sCDjVsmUNwnh_i3bgCq69",
    records =   "https://discord.com/api/webhooks/1294134671717957763/bEuXT5GqgiqP0HFkQHcFIwPDr6_elMhzF5nUCfWnWSZGI8hzHZ8fbSbEvVRdZ5ca0_1S",
    hostOpen =  "https://discord.com/api/webhooks/1294345171764248586/D3D2XTB9HL7n7iFV5xlykuX5CAVfc_Kg8p1M9vVQ9P7vNXAxHDEc3-VwrTuw_Fr4LrqL",
    adminCall = "https://discord.com/api/webhooks/1302312023660695552/yS0UJ01ukEQrI_-3P1Xj28ChU8i5U69sFO4g4pjfP_SWQqAFUBZt8Vij9CC0IvwSIGue",
    haxChat =   "https://discord.com/api/webhooks/1303160112403320842/xznye32Z3shmj7IBDcNOyCr6PeXWxGHlAC9omLLOc5TfLxHNJLs8MmHR6QoKBFDKxonO",
    entrys =    "https://discord.com/api/webhooks/1303436820759183411/ajsF-l71CeFYnWuzTVye6UlkpNpIONX-mdoBLZfwi541ptxORzRkztQ_C2JkMkk0lUUK"
) 

mainserver = Server(hostName="🟦🟦🟦 miku server juegan todos 🟦🟦🟦",
                    stadium=Stadiums.FUTSAL_X7, 
                    adminPassword="holasoyadmin",
                    filepath="files/script.js", 
                    gameTime=10, 
                    goalLimit=5, 
                    dsLinks=discordLinks)

testserver = Server(hostName="miku testing :3",
                    stadium=Stadiums.FUTSAL_X7, 
                    adminPassword="holasoyadmin",
                    filepath="files/script.js", 
                    gameTime=10, 
                    goalLimit=5, 
                    dsLinks=DiscordLinks())

# TODO: Control para usar el chat desde la consola

async def main():
    ui = UI()

    logger = Logs(datetime.now(), ui)
    server = testserver

    manager = Manager(logger, server, ui)

    ui.setInputCallback(manager.processInput)

    await ui.run()

if __name__ == "__main__":
    asyncio.run(main())