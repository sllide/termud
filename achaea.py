from interface.screen import Screen

class World(object):
    def __init__(self):
        self.host = "achaea.com"
        self.port = 23
        self.layoutWidth = 30
        self.layoutHeight = 15
        self.topWindows = [MapScreen, DescriptionScreen]
        self.sideWindows = [CharacterScreen, ItemScreen]

class MapScreen(Screen):
    def __init__(self):
        self.size = 30
        self.type = "redirect"
        self.trigger = "map"

class DescriptionScreen(Screen):
    def __init__(self):
        self.size = 60
        self.type = "gmcp"
        self.trigger = 'Room.Info'

    def handleGMCP(self, module, data):
        self.clear()
        if module == "Room.Info":
            self.printString("[" + data['name'] + "]\n")
            self.printString(data['desc'])

class CharacterScreen(Screen):
    def __init__(self):
        self.size = 20
        self.type = "gmcp"
        self.trigger = 'Char.Status'

    def handleGMCP(self, module, data):
        self.clear()
        if module == "Char.Status":
            self.printString("[" + data['fullname'] + "]" + "\n")
            self.printString("Age: " + data['age'] + "\n")
            self.printString("Race: " + data['race'] + "\n")
            self.printString("Class: " + data['class'] + "\n")
            self.printString("Level: " + data['level'] + "\n")
            self.printString("Gold: " + data['gold'] + "\n")
            self.printString("City: " + data['city'] + "\n")

class ItemScreen(Screen):
    def __init__(self):
        self.size = 30
        self.type = "gmcp"
        self.trigger = 'Char.Items.List'

    def handleGMCP(self, module, data):
        self.clear()
        if module == "Char.Items.List":
            self.printString("[Items]\n")
            for item in data['items']:
                self.printString(item['name'] + "\n")
