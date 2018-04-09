import socket

class Connection(object):
    def __init__(self):
        self.connected = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(False)
        self.packetBuffer = []

    def connect(self, host, port):
        try:
            self.socket.connect((host, port))
        except socket.error:
            pass
        self.connected = True

    def isConnected(self):
        return self.connected

    def receive(self):
        packet = ""
        try:
            while True:
                data = self.socket.recv(512)
                if not data:
                    break
                packet += data
        except socket.error:
            pass
        if packet:
            self.packetBuffer.append(packet)

    def getPacket(self):
        if len(self.packetBuffer) > 0:
            return self.packetBuffer.pop(0)
        return False

    def sendPacket(self, data):
        while data:
            try:
                sent = self.socket.send(data)
                data = data[sent:]
            except socket.error:
                pass
