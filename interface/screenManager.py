class ScreenManager(object):
    def __init__(self):
        self.topScreens = []
        self.sideScreens = []
        self.outputScreen = "main"
        self.redirects = {}
        self.gmcpCallbacks = {}

    def register(self, screen):
        self.screens.append(screen)

    def refresh(self):
        need = False
        for screen in self.topScreens:
            if screen.needsRefresh():
                need = True
                screen.refresh()
        for screen in self.sideScreens:
            if screen.needsRefresh():
                need = True
                screen.refresh()
        if self.input.needsRefresh():
            self.input.refresh()
            need = True
        if self.output.needsRefresh():
            self.output.refresh()
            need = True
        return need

    def registerInput(self, screen):
        self.input = screen

    def registerOutput(self, screen):
        self.output = screen

    def registerSideWindow(self, screen):
        self.sideScreens.append(screen)

    def registerTopWindow(self, screen):
        self.topScreens.append(screen)

    def registerWorld(self, world):
        self.world = world
        for screen in self.world.sideWindows:
            self.registerSideWindow(screen())
        for screen in self.world.topWindows:
            self.registerTopWindow(screen())

    def buildScreens(self, mainWindow, size):
        w, h = size
        self.buildOutputScreen(mainWindow, w, h)
        self.buildInputScreen(mainWindow, w, h)
        usedWidth = 0
        for screen in self.topScreens:
            if screen.type == "redirect":
                self.addRedirectCallback(screen.trigger, screen)
            if screen.type == "gmcp":
                self.addGMCPCallback(screen.trigger, screen)
            window = mainWindow.subwin(self.world.layoutHeight, screen.size, 0, usedWidth)
            usedWidth += screen.size
            window.scrollok(True)
            screen.registerScreen(window)
        usedHeight = 0
        for screen in self.sideScreens:
            if screen.type == "redirect":
                self.addRedirectCallback(screen.trigger, screen)
            if screen.type == "gmcp":
                self.addGMCPCallback(screen.trigger, screen)
            window = mainWindow.subwin(screen.size,self.world.layoutWidth,usedHeight,w-1-self.world.layoutWidth)
            usedHeight += screen.size
            window.scrollok(True)
            screen.registerScreen(window)

    def addGMCPCallback(self, trigger, screen):
        if not trigger in self.gmcpCallbacks:
            self.gmcpCallbacks.update({trigger: []})
        self.gmcpCallbacks[trigger].append(screen)

    def addRedirectCallback(self, trigger, screen):
        if not trigger in self.redirects:
            self.redirects.update({trigger: []})
        self.redirects[trigger].append(screen)

    def printString(self, string, color):
        if self.outputScreen in self.redirects:
            for screen in self.redirects[self.outputScreen]:
                screen.printString(string, color)
        else:
            self.output.printString(string, color)

    def parseGMCP(self, action):
        if action[1] in self.gmcpCallbacks:
            for screen in self.gmcpCallbacks[action[1]]:
                screen.handleGMCP(action[1], action[2])

    def setOutput(self, screen):
        self.outputScreen = screen

    def resizeScreens(self, size):
        pass

    def buildInputScreen(self, mainWindow, w, h):
        window = mainWindow.subwin(1,w-1,h-1,0)
        window.scrollok(True)
        self.input.registerScreen(window)

    def buildOutputScreen(self, mainWindow, w, h):
        layoutW = self.world.layoutWidth
        layoutH = self.world.layoutHeight
        window = mainWindow.subwin(h-1-layoutH,w-1-layoutW,layoutH,0)

        window.scrollok(True)
        self.output.registerScreen(window)
