#!/usr/bin/python
from interface import Interface
from system import System
from achaea import World

import traceback
import curses
from time import sleep

class Termud(object):

    def __init__(self):
        self.boot()
        self.loop()

    def boot(self):
        try:
            self.world = World()
            self.interface = Interface()
            self.interface.build(self.world)
            self.system = System(self.world)
        except:
            self.stop(traceback.format_exc())

    def loop(self):
        try:
            while True:
                sleep(1.0/30.0)
                self.step()
        except KeyboardInterrupt as e:
            self.stop("Gud bye!")
        except Exception as e:
            self.stop(traceback.format_exc())

    def step(self):
        #keyboard
        while True:
            key = self.interface.getch()
            if not key:
                break
            self.system.input(key)

        self.interface.setInput(self.system.getCommand())
        self.interface.step(self.system.step())

    def stop(self, reason=False):
        try:
            self.interface.stop()
        except:
            curses.endwin()
        if reason:
            print reason
        exit()

if __name__ == '__main__':
    Termud()
