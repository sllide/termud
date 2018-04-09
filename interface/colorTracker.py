import curses

class ColorTracker:
    def __init__(self):
        self.palet = {}
        self.iColor = 8
        self.bgColor = -1
        self.fgColor = 7
        self.bold = False

    def getColor(self):
        code = str(self.bgColor) + "." + str(self.fgColor)
        if not code in self.palet:
            curses.init_pair(self.iColor, self.fgColor, self.bgColor)
            self.palet[code] = self.iColor
            self.iColor += 1

        color = curses.color_pair(self.palet[code])
        if self.bold:
            color = color | curses.A_BOLD
        return color

    def updateColor(self, v):
        v = int(v)
        if v>=30 and v<=37:
            self.fgColor = v % 30
        elif v>=40 and v<=47:
            self.bgColor = v % 40
            if self.bgColor == 0:
                self.bgColor = -1
        elif v==0:
            self.bold = False
        elif v==1:
            self.bold = True
