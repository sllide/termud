from inputParser import InputParser
from networkParser import NetworkParser
from connection import Connection
import json

class System(object):
    def __init__(self):
        self.inputParser = InputParser()
        self.networkParser = NetworkParser()
        self.connection = Connection()
        self.output = ""

    def connect(self, host, port):
        self.connection.connect(host, port)

    def send(self, data):
        self.connection.sendPacket(data)

    def step(self):
        self.actions = []
        for line in self.inputParser.getOutput():
            if line[0] != '.':
                self.actions.append(['print', line + "\n"])
                self.send(line + "\n")
            else:
                self.connection.sendPacket("\xFF\xFA\xC9"+line[1:]+"\xFF\xF0")
        self.connection.receive()
        while True:
            packet = self.connection.getPacket()
            if not packet:
                break
            self.parsePacket(packet)
        return self.actions

    def parsePacket(self, packet):
        actions = self.networkParser.parse(packet)
        for action in actions:
            if action[0] == "send":
                self.send(action[1])
            if action[0] == "gmcp":
                split = action[1].split(' ', 1)
                if len(split)>1:
                    self.actions.append(["gmcp", split[0], json.loads(split[1])])
                else:
                    self.actions.append(["print", "no hablo gmcp\n"])
            else:
                self.actions.append(action)

    def input(self, key):
        self.inputParser.parse(key)

    def getInput(self):
        return self.inputParser.getCommand()
