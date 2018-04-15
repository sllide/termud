from random import Random
from screen import Screen
from collections import OrderedDict

class ScreenManager(object):
    def __init__(self):
        self.screens = OrderedDict()
        self.top = 0
        self.side = 0
        self.bottom = 0

    def registerWindow(self, name, position, size=False):
        self.screens.update({name: Screen(position, size, (name=="chat"))})

    def refresh(self):
        need = False
        for name, screen in self.screens.items():
            if screen.needsRefresh():
                need = True
                screen.refresh()
        return need

    def buildScreens(self, mainWindow, size, layoutSize):
        self.top = 0
        self.side = 0
        self.bottom = 0
        for name, screen in self.screens.items():
            if name != "main":
                self.buildScreen(mainWindow, size, screen, layoutSize)

        if "main" in self.screens:
            self.buildScreen(mainWindow, size, self.screens['main'], layoutSize)

    def buildScreen(self, mainWindow, size, screen, layoutSize):
        sw, sh = size
        sideWidth, topHeight = layoutSize 
        if screen.position == "bottom":
            x = sideWidth
            y = sh - 1 - self.bottom
            w = sw - sideWidth
            h = 1
            self.bottom += 1
        elif screen.position == "side":
            x = 0
            y = topHeight + self.side
            w = sideWidth
            h = screen.size
            self.side += h
        elif screen.position == "top":
            x = self.top
            y = 0
            w = screen.size
            h = topHeight
            self.top += w
        elif screen.position == "fill":
            x = sideWidth
            y = topHeight
            w = sw - sideWidth
            h = sh - topHeight - self.bottom
        else:
            what
        window = mainWindow.subwin(h,w,y,x)
        window.scrollok(True)
        screen.registerScreen(window)

    def fillScreens(self):
        random = Random()
        random.seed()
        for name, screen in self.screens.items():
            char = chr(random.randrange(32,126))
            screen.printString('')
            screen.screen.border(char, char, char, char, char, char, char, char)

    def getWindow(self, name):
        if name in self.screens:
            return self.screens[name]
        return False
