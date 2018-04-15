#!/usr/bin/python
from interface import Interface
from system import System
from world import World
from manager import Manager

import traceback
from time import sleep


class Termud(object):

    def __init__(self):
        self.log = open("log", 'w', 0)
        self.boot()
        self.bootWorld()
        self.loop()

    def boot(self):
        try:
            self.interface = Interface()
            self.system = System()
            self.manager = Manager(self.system, self.interface)
        except:
            self.stop('Failed to boot Termud:\n\n'+traceback.format_exc())

    def bootWorld(self):
        try:
            self.world = World()
            self.manager.setWorld(self.world)
            self.world.registerWindows(self.manager)
            self.interface.setLayoutSize(self.world.sidebarWidth, self.world.topbarHeight)
            self.interface.build()
            self.system.connect(self.world.host, self.world.port)
        except:
            self.stop('Failed to boot World:\n\n'+traceback.format_exc())

    def loop(self):
        try:
            while True:
                sleep(1.0/30.0)
                self.step()
        except KeyboardInterrupt as e:
            self.stop("Gud bye!")
        except Exception as e:
            self.stop('Runtime error:\n\n'+traceback.format_exc())

    def step(self):
        while True:
            key = self.interface.getch()
            if not key:
                break
            self.system.input(key)
            self.world.input(key, self.manager)
            self.interface.setInput(self.system.getInput())
        actions = self.system.step()
        self.interface.checkResize()
        for action in actions:
            self.log.write(str(action)+"\n")
            if action[0] == "connected":
                self.world.onConnect(self.manager)
            if action[0] == "gmcp":
                self.world.handleGMCP(action[1], action[2], self.manager)
            else:
                self.interface.step(action)
        self.interface.refresh()

    def stop(self, reason=False):
        try:
            self.interface.stop()
        except:
            try:
                import curses
                curses.endwin()
            except:
                pass
        if reason:
            print reason
        exit()

if __name__ == '__main__':
    import locale
    locale.setlocale(locale.LC_ALL, '')
    Termud()
