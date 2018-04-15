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
        self.layoutWidth = 0
        self.layoutHeight = 0
        self.outputWindow = 'main'

    def getColorTracker(self):
        return self.colorTracker

    def getWindow(self, name):
        return self.screenManager.getWindow(name)

    def createWindow(self, name, position, size=False):
        self.screenManager.registerWindow(name,position,size)

    def setLayoutSize(self, width, height):
        self.layoutWidth = width
        self.layoutHeight = height

    def build(self):
        mainScreen = self.curses.getMainScreen()
        size = self.curses.getSize()
        self.screenManager.buildScreens(mainScreen, size, (self.layoutWidth, self.layoutHeight))

    def stop(self):
        self.curses.stop()

    def getch(self):
        return self.curses.getch()

    def setInput(self, string):
        if string != self.currentInput:
            self.screenManager.getWindow('input').clear()
            self.screenManager.getWindow('input').printString(string)
            self.currentInput = string

    def checkResize(self):
        if self.curses.isResized():
            self.build()

    def setOutputWindow(self, name):
        self.outputWindow = name

    def getOutputWindow(self):
        return self.outputWindow

    def step(self, action):
        if action[0] == "print":
            self.screenManager.getWindow(self.outputWindow).printString(action[1], self.colorTracker.getColor())
        elif action[0] == "color":
            self.colorTracker.updateColor(action[1])

    def refresh(self):
        if self.screenManager.refresh():
            self.curses.refresh()
