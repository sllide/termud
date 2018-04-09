import curses

class CursesHelper(object):
    def __init__(self):
        self.running = False

    def start(self):
        self.screen = curses.initscr()
        self.screen.keypad(True)
        self.screen.nodelay(True)

        curses.start_color()
        curses.use_default_colors()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        
        self.running = True

    def getSize(self):
        (y, x) = self.screen.getmaxyx()
        return (x, y)

    def refresh(self):
        curses.doupdate()

    def stop(self):
        if not self.running:
            return
        curses.endwin()

    def getMainScreen(self):
        return self.screen

    def isRunning(self):
        return self.running

    def getch(self):
        char = self.screen.getch()
        if char == -1:
            return False
        return char
