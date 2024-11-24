class Commander:
    def __init__(self, scheduler, driver, server):
        self.scheduler = scheduler
        self.driver = driver
        self.server = server

    def processInput(self, message):
        if (message) == "/startserver":
            self.scheduler.startServer()