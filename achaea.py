from interface.screen import Screen

class World(object):
    def __init__(self):
        self.host = "achaea.com"
        self.port = 23
        self.layoutWidth = 22
        self.layoutHeight = 0
        self.topWindows = []
        self.sideWindows = [MapScreen, CharacterScreen]

class MapScreen(Screen):
    def __init__(self):
        self.size = 15
        self.type = "redirect"
        self.trigger = "map"

class CharacterScreen(Screen):
    def __init__(self):
        self.size = 0
        self.type = "gmcp"
        self.trigger = ['Char.Status']

    def handleGMCP(self, module, data):
        self.printString(module + "\n")
