class InputParser(object):

    def __init__(self):
        self.output = []
        self.command = ""

    def parse(self, key):
        if key>31 and key<127:
            self.command += chr(key)

        elif key==10:
            self.output.append(self.command)
            self.command = ""

        elif key==263:
            self.command = self.command[:-1]

        else:
            return key

    def getOutput(self):
        output = self.output
        self.output = []
        return output

    def getCommand(self):
        return self.command
