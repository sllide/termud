class Screen(object):

    def __init__(self, position, size=False, isMap=False):
        self.position = position
        self.size = size
        self.lineBuffer = []
        self.bufferSize = 200
        self.isMap = isMap

    def registerScreen(self, screen):
        self.screen = screen
        for line in self.lineBuffer:
            self.printString(line['content'], line['color'], False)
        self.needRefresh = True

    def refresh(self):
        self.needRefresh = False
        self.screen.noutrefresh()
    
    def printString(self, string, color=False, writeBuffer=True):
        self.needRefresh = True
        if self.isMap:
            string = string.replace('\n', '').replace('\r', '')
            if len(string)>0:
                string += '\n'
        if writeBuffer:
            self.lineBuffer.append({'content': string, 'color': color})
            length = len(self.lineBuffer)
            if length>self.bufferSize:
                self.lineBuffer = self.lineBuffer[length-self.bufferSize:]
        try:
            if color:
                self.screen.addstr(string.encode('utf-8'), color)
            else:
                self.screen.addstr(string.encode('utf-8'))
        except:
            pass

    def clear(self):
        self.lineBuffer = []
        self.screen.clear()
        self.needRefresh = True

    def needsRefresh(self):
        return self.needRefresh
    
    def getSize(self):
        y,x = self.screen.getmaxyx()
        return (x, y)
