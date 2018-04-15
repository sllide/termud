# -*- coding: UTF-8 -*-
class World(object):
    def __init__(self):
        self.log = open('world', 'w', 0)
        self.host = "achaea.com"
        self.port = 23
        self.sidebarWidth = 22
        self.topbarHeight = 15
        self.status = {}
        self.vitals = {}
        self.inventory = {}
        self.roomItems = {}
        self.roomInfo = {}
        self.roomPlayers = {}

    def onConnect(self, manager):
        manager.sendGMCP('Core.Hello {"Client":"Termud","Version":"0.1"}')
        manager.sendGMCP('Core.Supports.Set ["IRE.Time 1", "Core 1", "Char 1", "Char.Afflictions 1", "Char.Defences 1", "Char.Items 1", "Char.Skills 1", "Comm.Channel 1", "Room 1", "Redirect 1"]')
    
    def registerWindows(self, manager):
        manager.createWindow("input", "bottom")
        manager.createWindow("status", "bottom")
        manager.createWindow("map", "top", 22)
        manager.createWindow("roominfo", "top", 70)
        manager.createWindow("roomitems", "top", 30)
        manager.createWindow("chat", "top")
        manager.createWindow("player", "side")
        manager.createWindow("main", "fill")
    
    def handleGMCP(self, module, data, manager):
        if module == "Char.Vitals":
            self.vitals.update({'hp': [data['hp'], data['maxhp']]})
            self.vitals.update({'mp': [data['mp'], data['maxmp']]})
            self.vitals.update({'ep': [data['ep'], data['maxep']]})
            self.vitals.update({'wp': [data['wp'], data['maxwp']]})
            manager.updateWindow("status")

        elif module == "Char.Items.List":
            if data['location'] == 'room':
                self.roomItems = {}
                for item in data['items']:
                    self.roomItems.update({item['id']: item})
                manager.updateWindow('roomitems')
            elif data['location'] == 'inv':
                self.inventory = {}
                for item in data['items']:
                    self.inventory.update({item['id']: item})
                manager.updateWindow('player')

        elif module == "Char.Items.Add":
            item = data['item']
            if data['location'] == 'inv':
                self.inventory.update({item['id']: item})
                manager.updateWindow('player')
            if data['location'] == 'room':
                self.roomItems.update({item['id']: item})
                manager.updateWindow('roomitems')

        elif module == "Char.Items.Remove":
            item = data['item']
            if data['location'] == 'inv':
                if item['id'] in self.inventory:
                    del self.inventory[item['id']]
                manager.updateWindow('player')
            if data['location'] == 'room':
                if item['id'] in self.roomItems:
                    del self.roomItems[item['id']]
                manager.updateWindow('roomitems')

        elif module == "Room.Players":
            self.roomPlayers = {}
            for player in data:
                self.roomPlayers.update({player['name']: player['fullname']})
            manager.updateWindow('roominfo')

        elif module == "Room.AddPlayer":
            self.roomPlayers.update({data['name']: data['fullname']})
            manager.updateWindow('roominfo')

        elif module == "Room.RemovePlayer":
            if data in self.roomPlayers:
                del self.roomPlayers[data]
            manager.updateWindow('roominfo')

        elif module == "Room.Info":
            self.roomInfo = data
            manager.updateWindow('roominfo')

        elif module == "Redirect.Window":
            manager.setOutputWindow(data)

        elif module == "Comm.Channel.Start":
            self.storedWindow = manager.getOutputWindow()
            manager.setOutputWindow('chat')

        elif module == "Comm.Channel.End":
            manager.setOutputWindow(self.storedWindow)

        self.log.write('\n'+module+'\n')
        self.log.write(str(data)+'\n')

    def input(self, key, manager):
        if key == 9:
            manager.printString('tab pressed\n')

    def updateWindow(self, name, screen, colorTracker):
        if name == "status":
            w,h = screen.getSize()
            w = w - 10
            screen.clear()
            colorTracker.storeColor()
            self.printBar('hp', screen, colorTracker, w/4)
            self.printBar('mp', screen, colorTracker, w/4)
            self.printBar('ep', screen, colorTracker, w/4)
            self.printBar('wp', screen, colorTracker, w/4)
            colorTracker.restoreColor()

        if name == "roominfo":
            screen.clear()
            screen.printString(self.roomInfo['area'] + '\n')
            screen.printString(self.roomInfo['name'] + ' [ ' + self.roomInfo['environment'] + ' ]\n\n')
            mobs = []
            players = []
            for key, item in self.roomItems.items():
                if 'attrib' in item and 'm' in item['attrib'] and not 'd' in item['attrib']:
                    mobs.append(item['name'])
            for key, name in self.roomPlayers.items():
                players.append(key)
            screen.printString("Mobs:".ljust(35) + "Players:\n")
            for i in range(0, max(len(mobs),len(players))):
                if i<len(mobs):
                    mob = mobs[i]
                else:
                    mob = ""
                if i<len(players):
                    player = players[i]
                else:
                    player = ""
                screen.printString(mob.ljust(35) + player + '\n')

    def printBar(self, stat, screen, color, w):
        if stat == "hp":
            colors = [1,30,41]
        elif stat == "mp":
            colors = [1,30,44]
        elif stat == "ep":
            colors = [1,30,43]
        elif stat == "wp":
            colors = [1,30,42]
        v, maxv = self.vitals[stat]
        string = (' ' + stat + ': ' + v + '/' + maxv).ljust(w-2) 
        filledWidth = int(round(float(v) / float(maxv) * float(w)))
        left = string[:filledWidth]
        right = string[filledWidth:]
        screen.printString('[')
        for c in colors:
            color.updateColor(c)
        screen.printString(left, color.getColor())
        color.updateColor(0)
        color.updateColor(1)
        screen.printString(right, color.getColor())
        screen.printString(']')
