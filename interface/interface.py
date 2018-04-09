from cursesHelper import CursesHelper
from colorTracker import ColorTracker
from screenManager import ScreenManager
from screen import Screen

import curses

class Interface(object):
    def __init__(self):
        self.curses = CursesHelper()
        self.screenManager = ScreenManager()
        self.colorTracker = ColorTracker()
        self.curses.start()
        self.currentInput = ""
        self.outputWindow = 'main'

    def build(self, world):
        self.world = world
        self.size = self.curses.getSize()
        self.buildUi()

    def buildUi(self):
        self.inputScreen = Screen()
        self.outputScreen = Screen()
        self.screenManager.registerInput(self.inputScreen)
        self.screenManager.registerOutput(self.outputScreen)
        self.screenManager.registerWorld(self.world)
        self.screenManager.buildScreens(self.curses.getMainScreen(), self.size)

    def refresh(self):
        if self.screenManager.refresh():
            self.curses.refresh()

    def stop(self):
        self.curses.stop()

    def getch(self):
        return self.curses.getch()

    def setInput(self, string):
        if string != self.currentInput:
            self.inputScreen.clear()
            self.inputScreen.printString(string)
            self.currentInput = string

    def step(self, actions):
        for action in actions:
            if action[0] == "print":
                if self.outputWindow == "map":
                    self.screenManager.map.printString(action[1], self.colorTracker.getColor())
                else:
                    self.outputScreen.printString(action[1], self.colorTracker.getColor())
            elif action[0] == "color":
                self.colorTracker.updateColor(action[1])
            elif action[0] == "redirect":
                self.outputWindow = action[1]
            else:
                self.outputScreen.printString("\nunknown action: " + str(action) + "\n\n")
        self.refresh()
