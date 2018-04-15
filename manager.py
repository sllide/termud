class Manager(object):
    OUTPUT_LAZY = 1
    OUTPUT_STRIP = 2

    def __init__(self, system, interface):
        self.system = system
        self.interface = interface

    def setWorld(self, world):
        self.world = world

    def createWindow(self, name, position, size=False):
        self.interface.createWindow(name, position, size)

    def updateWindow(self, name):
        window = self.interface.getWindow(name);
        if window:
            self.interface.getColorTracker().storeColor()
            self.world.updateWindow(name, window, self.interface.getColorTracker())
            self.interface.getColorTracker().restoreColor()

    def setOutputWindow(self, name):
        self.interface.setOutputWindow(name)

    def getOutputWindow(self):
        return self.interface.getOutputWindow()

    def printString(self, string):
        self.interface.getWindow('main').printString(string)

    def send(self, data):
        self.system.send(data + "\n")

    def sendGMCP(self, data):
        self.system.send("\xFF\xFA\xC9"+data+"\xFF\xF0")

    def setOutputMode(self, mode):
        return
        self.interface.setOutputMode(mode)
