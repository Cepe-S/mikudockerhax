from typing import List
from server_enums.OutputType import OutputType as outType

from Logs import Logs

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.command import Command
from selenium.common.exceptions import WebDriverException

import logging
from sys import platform
import os

DEFAULT_ARGUMENTS = ["--no-sandbox",
                     "--disable-dev-shm-usage",
                     "--headless",
                     "--log-level=3",
                     "--silent",
                     "--disable-logging",
                     "--enable-unsafe-swiftshader",
                    #  '--disable-setuid-sandbox',
                    #  '--disable-features=WebRtcHideLocalIpsWithMdns',
                    #  '--disable-component-extensions-with-background-pages',
                    #  '--disable-extensions',
                    #  '--disable-background-networking',
                    #  '--disable-hang-monitor',
                     '--mute-audio',
                    #  '--no-first-run',
                    #  '--disable-background-networking',
                    #  '--disable-breakpad',
                    #  '--disable-component-update',
                    #  '--disable-domain-reliability',
                    #  '--disable-sync',
                    #  '--metrics-recording-only',
                    #  '--no-zygote',
                    #  '--in-process-gpu',
                    #  '--allow-insecure-localhost', # may be a security risk idk :3
                    #  '--disable-low-res-tiling',
                     '--disable-gpu',
                     '--no-crash-upload',
                     '--disable-crash-reporter',
                    #  '--disable-client-side-phishing-detection',
                    #  '--disable-backgrounding-occluded-windows',
                    #  '--disable-background-timer-throttling',
                    #  '--disable-renderer-backgrounding',
                    #  '--disable-oopr-debug-crash-dump'
                    ]

DEFAULT_PATH = "/usr/bin/chromedriver"

class WebDriver:
    def __init__(self, arguments: List[str] = DEFAULT_ARGUMENTS, executablePath: str = DEFAULT_PATH, logger: Logs = None, runInContainer: bool = False):

        driverLogPath = "logs/driverLogs.txt"

        driverLogger = logging.getLogger('selenium')
        driverLogger.setLevel(logging.DEBUG)
        
        handler = logging.FileHandler(driverLogPath)
        driverLogger.addHandler(handler)

        logging.getLogger('selenium.webdriver.remote').setLevel(logging.WARN)
        logging.getLogger('selenium.webdriver.common').setLevel(logging.DEBUG)
        logging.getLogger('selenium.webdriver.chrome').setLevel(logging.CRITICAL)

        
        
        if not runInContainer:
            options = webdriver.ChromeOptions()
            for arg in arguments:
                options.add_argument(arg)
            
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
            options.add_experimental_option("detach", True)

            if "linux" in platform and executablePath:
                service = webdriver.ChromeService(executable_path=executablePath, log_output=os.devnull)
            else:
                service = webdriver.ChromeService(log_output=os.devnull)

            self.wd = webdriver.Chrome(service=service, 
                                       options=options,
                                       keep_alive=True)

        if runInContainer:
            options = webdriver.FirefoxOptions()

            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-web-security")
            # options.add_argument("--allow-running-insecure-content")
            # options.add_argument("--disable-blink-features=AutomationControlled")
            # options.set_preference("media.navigator.streams.fake", True)
            # options.set_preference("media.navigator.permission.disabled", True)
            # options.set_preference("media.autoplay.default", 0)
            # options.set_preference("media.volume_scale", 0)
            # options.set_preference("media.peerconnection.enabled", True)  # Habilitar WebRTC
            # options.set_preference("media.peerconnection.ice.obfuscate_host_addresses", False)  # Mostrar direcciones ICE

            options.set_capability("moz:firefoxOptions", {"args": []})
            print("Creating driver...")
            self.wd = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',
                                       options=options)

            try:
                print("Conectando al servidor Selenium...")
                self.wd.get("about:blank")
                print("Conexión exitosa al servidor Selenium.")
            except WebDriverException as e:
                print(f"Error al conectar al servidor Selenium: {e}")
                raise RuntimeError("No se pudo conectar al servidor Selenium.")
        
        self.logger = logger

    def getPage(self, page: str):
        self.wd.get(page)

    def refreshPage(self):
        self.wd.refresh()

    def minimizeWindow(self):
        self.wd.minimize_window()

    def runScript(self, script: str):
        self.wd.execute_script(script)

    def getConsoleLogs(self, printLogs: bool) -> str:
        logs = self.wd.get_log("browser")
        if printLogs and self.logger:
            for entry in logs:
                log = f"{entry['level']}: {entry['message']}"
                self.logger.addLog(log, outType=outType.SERVER)
        return logs 

    def findElementByCSS(self, path: str, time: int = 10) -> WebElement:    
        try:
            return WebDriverWait(self.wd, time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, path))
            )
        except NoSuchElementException:
            return None

    def findElementByXPath(self, path: str, time: int = 10) -> WebElement:
        try:
            return WebDriverWait(self.wd, time).until(
                EC.presence_of_element_located((By.XPATH, path))
            )
        except NoSuchElementException:
            return None

    def switchToFrame(self, frame: WebElement):
        self.wd.switch_to.frame(frame)

    def isDriverAlive(self) -> bool:
        try:
            self.wd.execute(Command.REFRESH)
            return True
        except Exception as error:
            self.logger.addLog(f"Can't connect with driver:\n {error}", outType=outType.ERROR)
            return False