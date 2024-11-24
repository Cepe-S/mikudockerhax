from WebDriver import WebDriver as wd
from ServerDoctor import ServerDoctor as Doctor
from UI import UI
from Server import Server
from Logs import Logs as Logger

from server_enums.OutputType import OutputType as outType

from time import sleep
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import inspect
import gc

class Manager:
    def __init__(self, logger: Logger, server: Server, ui: UI):
        self.logger = logger
        self.driver = wd(logger=self.logger, runInContainer=True)
        self.server = server
        self.ui = ui
        self.scheduler = AsyncIOScheduler()
        self.doctor = None
        self.isServerRunning = None
        self.serverLink = ""

    def runServer(self) -> int:
        try:
            if not self.isTokenValid(self.server.token):
                return 1

            self.ui.toConsole("Initializing server", outType.PROGRAM, True)

            page = "https://www.haxball.com/headless"
            self.driver.getPage(page)
            self.ui.toConsole(f"Page {page} connected.", outType.PROGRAM, False)

            # self.scheduler.add_job(self.driver.getConsoleLogs, 'interval', seconds=2, args=[True])
            # self.scheduler.start()
            # self.ui.toConsole("Logger executed", outType.PROGRAM, False)

            while not self.driver.isDriverAlive():
                self.ui.toConsole("The driver is not responding, trying again...", outType=outType.ERROR, bold=True)
                sleep(3)
            self.ui.toConsole("Driver checked", outType=outType.PROGRAM, bold=False)

            sleep(5)
            script = self.server.getScript()

            while not self.serverLink:
                self.driver.runScript(script)
                self.ui.toConsole("Script ejecuted", outType.PROGRAM, False)

                sleep(3)

                self.serverLink = self.server.getServerLink(self.driver)
                if not self.serverLink:
                    self.ui.toConsole(f"Can't find server link ~(>_<。)＼, trying again...", outType.ERROR, True)
                    self.driver.refreshPage()
                    sleep(3)

            self.ui.toConsole(f"Link found: {self.serverLink}", outType.PROGRAM, True)

            self.driver.minimizeWindow() # maybe it helps?
            self.isServerRunning = True

            # self.doctor = Doctor(self.serverLink, self.server.adminPassword, self.logger)
            # loop = asyncio.get_event_loop()
            # loop.run_in_executor(None, self._run_execute_doctor)  # Llama a un método que no es async

            self.ui.toConsole("Doctor executed", outType.PROGRAM, False)

            return 0

        except Exception as e:
            self.ui.toConsole(f"Error en el servidor: {str(e)}", outType.ERROR, True)
            return 1
        
    def _run_execute_doctor(self):
        asyncio.run(self.executeDoctor())
    
    async def executeDoctor(self):
        serverStopped = await self.doctor.getIntoPatient()
        
        if serverStopped:
            self.restartServer()

    def runServerScript(self):

        script = self.server.getScript()
        print(f"runnning a script of {len(script)} characters")
        print(self.driver.wd.execute_script("""
            var script = document.createElement('script');
            script.type = 'text/javascript';
            script.text = arguments[0];
            document.head.appendChild(script);
        """, script))
    
    def getHaxBallPage(self):
        self.driver.getPage("https://www.haxball.com/headless")

    def restartDriver(self):
        self.driver.wd.close()
        self.driver.wd.quit()
        self.driver = wd(logger=self.logger)

    def checkServerStatus(self):
        if not self.isServerRunning:
            self.ui.toConsole("Server is not running", outType.ERROR, True)
            return

        self.ui.toConsole("Server check done, everything fine n_n/", outType.PROGRAM, False)

    def startServer(self):
        self.runServer()

    def stopServer(self):
        self.ui.toConsole("Cerrando servidor", outType.PROGRAM, True)

        self.serverLink = ""

        if self.doctor.driver and self.doctor.driver.wd:
            self.doctor.driver.wd.close()
            self.doctor.driver.wd.quit()
        self.doctor = None

        if self.driver and self.driver.wd:
            self.driver.wd.close()
            self.driver.wd.quit()
        self.driver = wd(logger=self.logger)

        self.scheduler.remove_all_jobs()
        self.scheduler.shutdown(wait=False)
        self.scheduler = AsyncIOScheduler()

        gc.collect()

        self.ui.toConsole("Servidor cerrado", outType.PROGRAM, True)

    def sillyStopServer(self):
        self.ui.toConsole("Cerrando servidor", outType.PROGRAM, True)
        
        self.driver.wd.quit()
        self.driver = wd(logger=self.logger)

        sleep(5)
        self.ui.toConsole("Servidor cerrado", outType.PROGRAM, True)

    def restartServer(self):
        self.stopServer()
        self.startServer()

    def isTokenValid(self, token: str):
        self.ui.toConsole("Validating token", outType.PROGRAM, True)
        with open("files/token_validator.js", "r") as file:
            validatorScript = file.read().replace("{{token}}", token)

        driver = wd()

        driver.getPage("https://html5.haxball.com/headless")
        driver.runScript(validatorScript)

        for _ in range(10):
            consoleLogs = driver.getConsoleLogs(False)
            for entry in consoleLogs:
                response = entry["message"]

                if "Token is invalid" in response:
                    self.ui.toConsole("The token is invalid, please update the token with [updatetoken]", outType.ERROR, True)
                    driver.wd.close()
                    return False
                
                if "Valid token" in response:
                    self.ui.toConsole("Token validated", outType.PROGRAM, True)
                    driver.wd.close()
                    return True
                
            sleep(3)

        self.ui.toConsole("No response from token validator", outType.ERROR, True)

    def updateToken(self, token):
        if not len(token) == 39 and token[4] == '.':
            self.ui.toConsole("Wrong token format", outType.ERROR, True)
            return
        
        with open("files/token.txt", "w") as file:
            file.write(token)
        self.server.token = token
        self.ui.toConsole("Token updated", outType.PROGRAM, True)

    def testScriptRun(self):
        self.driver.runScript("console.log('Ejecutando script en el contexto principal');")

    def switchToHeadlessFrame(self):
        IFrame = self.driver.findElementByXPath("//iframe[contains(@src, 'headless.html')]")
        self.driver.switchToFrame(IFrame)

    def getLogs(self):
        logs = self.driver.wd.get_log("browser")
        for log in logs:
            print(log)

    def processInput(self, message: str):
        parts = message.split(' ')  
        command = parts[0]
        args = parts[1:]

        commands = {
            "startserver": self.startServer,
            "stopserver": self.stopServer,
            "restartserver": self.restartServer,
            "checkserver": self.checkServerStatus,
            "updatetoken": self.updateToken,
            "getpage": self.getHaxBallPage,
            "runscript": self.runServerScript,
            "getlogs": self.getLogs,
            "testScript": self.testScriptRun,
            "switchToHeadlessFrame": self.switchToHeadlessFrame,
            "sillystop": self.sillyStopServer
        }
        func = commands.get(command)

        if func:
            # obtiene el número de argumentos que necesita la función
            sig = inspect.signature(func)
            required_args = len([param for param in sig.parameters.values() if param.default == inspect.Parameter.empty])

            if len(args) == required_args:
                func(*args)
            else:
                self.ui.toConsole(f"El comando '{command}' espera {required_args} argumento(s), pero se recibieron {len(args)}.", outType.ERROR, True)
        else:
            self.ui.toConsole(f"Comando '{command}' no reconocido", outType.ERROR, True)

    def closeProgram(self):
        self.driver.wd.quit()
        self.scheduler.shutdown(wait=False)