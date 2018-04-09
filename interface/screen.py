class Screen(object):

    def registerScreen(self, screen):
        self.screen = screen
        self.needRefresh = True

    def refresh(self):
        self.needRefresh = False
        self.screen.noutrefresh()
    
    def printString(self, string, color=False):
        self.needRefresh = True
        string = str(string)
        if color:
            self.screen.addstr(string, color)
        else:
            self.screen.addstr(string)

    def clear(self):
        self.screen.clear()

    def needsRefresh(self):
        return self.needRefresh
