from curses.ascii import isprint
import re

class NetworkParser(object):
    def __init__(self):
        self.negotiationRegexp = re.compile("\xFF(\xFB|\xFD|\xFC)(.)")
        self.colorRegexp = re.compile("\x1B\[((\d+)(;|))+m")
        self.numberRegexp = re.compile("\d+")
        self.gmcpRegexp = re.compile("\xFF\xFA\xC9(.+?)\xFF\xF0")
        self.crRegexp = re.compile("\r")
        self.goAheadRegexp = re.compile("\xFF\xF9")
        self.handShook = False
        self.log = open('parser', 'w', 0)

    def parse(self, packet):
        self.actions = []
        packet = self.crRegexp.sub('', packet)
        packet = self.goAheadRegexp.sub('', packet)
        while True:
            negotiation = self.negotiationRegexp.search(packet)
            color = self.colorRegexp.search(packet)
            gmcp = self.gmcpRegexp.search(packet)

            if negotiation and negotiation.start() == 0:
                self.negotiateFeature(negotiation.group(1), negotiation.group(2))
                packet = packet[negotiation.end():]
            elif color and color.start() == 0:
                self.parseColor(color.group())
                packet = packet[color.end():]
            elif gmcp and gmcp.start()  == 0:
                self.actions.append(['gmcp', gmcp.group(1)])
                self.log.write("\nGOT GMCP:\n"+gmcp.group(1))
                packet = packet[gmcp.end():]
            else:
                if packet:
                    lowest = 99999
                    if negotiation and lowest > negotiation.start():
                        lowest = negotiation.start()
                    if color and lowest > color.start():
                        lowest = color.start()
                    if gmcp and lowest > gmcp.start():
                        lowest = gmcp.start()
                    self.actions.append(['print', packet[:lowest]])
                    packet = packet[lowest:]
                else:
                    break
        if not self.handShook:
            self.actions.append(['connected'])
            self.handShook = True
        return self.actions
    
    def parseColor(self, match):
        for color in self.numberRegexp.finditer(match):
            self.actions.append(['color', int(color.group())])

    def negotiateFeature(self, mode, feature):
        if mode == "\xFB":
            if feature == "\xC9": #will do gmcp
                self.actions.append(['send', "\xFF\xFD\xC9"])
            else:
                self.actions.append(['send', "\xFF\xFE"+feature])
            return
        if mode == "\xFD":
            self.actions.append(['send',"\xFF\xFC" + feature])
            return
