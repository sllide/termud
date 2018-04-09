from inputParser import InputParser
from networkParser import NetworkParser
from connection import Connection
import json

class System(object):
    def __init__(self, world):
        self.world = world
        self.inputParser = InputParser()
        self.networkParser = NetworkParser()
        self.connection = Connection()
        self.connection.connect(world.host,world.port)
        self.output = ""

    def step(self):
        self.unparsedActions = []
        for line in self.inputParser.getOutput():
            self.unparsedActions.append(['print', "\n"])
            self.connection.sendPacket(line + "\n")
        self.connection.receive()
        while True:
            packet = self.connection.getPacket()
            if not packet:
                break
            self.parsePacket(packet)
        return self.unparsedActions

    def parsePacket(self, packet):
        actions = self.networkParser.parse(packet)
        for action in actions:
            if action[0] == "send":
                self.connection.sendPacket(action[1])
            elif action[0] == "gmcp":
                if action[1].find("Redirect.Window")>-1:
                    self.unparsedActions.append(["redirect", action[1].split(' ', 1)[1][1:-1]])
                else:
                    self.unparsedActions.append([action[0], action[1].split(' ', 1)[0], json.loads(action[1].split(' ', 1)[1])])

            else:
                self.unparsedActions.append(action)

    def input(self, key):
        self.inputParser.parse(key)

    def getCommand(self):
        return self.inputParser.getCommand()
