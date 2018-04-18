# -*- coding: UTF-8 -*-
class World(object):
    def __init__(self):
        self.log = open('world', 'w', 0)
        self.host = "achaea.com"
        self.port = 23
        self.sidebarWidth = 38
        self.topbarHeight = 18
        self.items = {}
        self.players = {}
        self.inventory = {}
        self.time = {}
        self.room = {}
        self.status = {}
        self.vitals = {}
        self.icons = {
            'humanoid': u'',
            'animal': u'',
            'plant': u'',
            'mineral': u'ﱦ',
            'scroll': u'',
            'mug': u'',
            'shrine': u'',
            'coin': u'',
            'container': u'ﰤ',
            'clothing': u'',
            'crystal': u'',
            'door': u'ﴘ',
            'fiend': u'',
            'guard': u'ﲅ',
            'lamp': u'﮳',
            'magical': u'',
            'curative': u'',
            'monster': u'ﯙ',
            'deadbody': u'ﮊ',
            'food': u'ﴨ',
            'hp': u'',
            'mp': u'',
            'ep': u'',
            'wp': u'',
            'key': u'',
            'potion': u'',
            'weapon': u'理',
            'player': u'',
            'profile': u'',
            'rune': u'',
            'commodity': u'',
        }

    def onConnect(self, manager):
        manager.sendGMCP('Core.Hello {"Client":"Termud","Version":"0.1"}')
        manager.sendGMCP('Core.Supports.Set ["IRE.Time 1", "Core 1", "Char 1", "Char.Afflictions 1", "Char.Defences 1", "Char.Items 1", "Char.Skills 1", "Comm.Channel 1", "Room 1", "Redirect 1"]')
    
    def registerWindows(self, manager):
        manager.createWindow("input", "bottom")
        manager.createWindow("map", "top", 38)
        manager.createWindow("items", "top", 35)
        manager.createWindow("mobs", "top", 35)
        manager.createWindow("chat", "top")
        manager.createWindow("area", "side", 6)
        manager.createWindow("player", "side")
        manager.createWindow("main", "fill")
    
    def handleGMCP(self, module, data, manager):
        #WINDOW REDIRECTS
        if module == "Redirect.Window":
            manager.setOutputWindow(data)

        elif module == "Comm.Channel.Start":
            self.storedWindow = manager.getOutputWindow()
            manager.setOutputWindow('chat')

        elif module == "Comm.Channel.End":
            manager.setOutputWindow(self.storedWindow)

        #ITEM TRACKING
        elif module == "Char.Items.List":
            if data['location'] == 'room':
                self.items = {}
                for item in data['items']:
                    self.items.update({item['id']: item})
                manager.updateWindow('items')
                manager.updateWindow('mobs')
            if data['location'] == 'inv':
                self.inventory = {}
                for item in data['items']:
                    self.inventory.update({item['id']: item})
                manager.updateWindow('player')

        elif module == "Char.Items.Add":
            item = data['item']
            if data['location'] == 'room':
                self.items.update({item['id']: item})
                manager.updateWindow('items')
                manager.updateWindow('mobs')
            if data['location'] == 'inv':
                self.inventory.update({item['id']: item})
                manager.updateWindow('player')

        elif module == "Char.Items.Remove":
            item = data['item']
            if data['location'] == 'room':
                if item['id'] in self.items:
                    del self.items[item['id']]
                    manager.updateWindow('items')
                    manager.updateWindow('mobs')
            if data['location'] == 'inv':
                if item['id'] in self.inventory:
                    del self.inventory[item['id']]
                manager.updateWindow('player')

        #PLAYER TRACKING
        elif module == "Room.Players":
            self.players = {}
            for player in data:
                self.players.update({player['name']: player['fullname']})
            manager.updateWindow('mobs')

        elif module == "Room.AddPlayer":
            self.players.update({data['name']: data['fullname']})
            manager.updateWindow('mobs')

        elif module == "Room.RemovePlayer":
            if data in self.players:
                del self.players[data]
            manager.updateWindow('mobs')

        #AREA INFO
        elif module == "Room.Info":
            self.room = data
            manager.updateWindow('area')

        elif module == "IRE.Time.List":
            self.time.update(data)
            manager.updateWindow('area')

        elif module == "IRE.Time.Update":
            self.time.update(data)
            manager.updateWindow('area')

        #PLAYER INFO
        elif module == "Char.Status":
            self.status.update(data)
            manager.updateWindow('player')

        elif module == "Char.Vitals":
            self.vitals.update(data)
            manager.updateWindow('player')

        #GMCP LOGGING
        self.log.write('\n'+module+'\n')
        self.log.write(str(data)+'\n')

    def updateWindow(self, name, screen, color):
        if name == "items":
            screen.clear()
            screen.printString('[ROOM ITEMS]\n')
            for key, item in self.items.items():
                if not 'attrib' in item or not 'm' in item['attrib'] or 'd' in item['attrib']:
                    if 'icon' in item:
                        screen.printString(self.getIcon(item['icon']) + ' ')
                    screen.printString(self.cutString(item['name'], 30) + '\n')

        elif name == "mobs":
            screen.clear()
            screen.printString('[ROOM MOBS]\n')
            for key, name in self.players.items():
                color.updateColor(31)
                screen.printString(self.getIcon('player') + ' ' + self.cutString(name, 30) + '\n', color.getColor())
            for key, item in self.items.items():
                if 'attrib' in item and 'm' in item['attrib'] and not 'd' in item['attrib']:
                    if 'icon' in item:
                        screen.printString(self.getIcon(item['icon']) + ' ')
                    screen.printString(self.cutString(item['name'], 30) + '\n')

        elif name == "area":
            screen.clear()
            if 'area' in self.room and 'time' in self.time:
                screen.printString('[ ' + self.room['area'] + ' ]\n')
                screen.printString(self.room['name'] + '\n')

        elif name == "player":
            screen.clear()
            w,h = screen.getSize()
            if not 'name' in self.status or not 'hp' in self.vitals:
                return
            screen.printString('[ ' + self.status['fullname'] + ' ] \n')
            screen.printString('Age: ' + self.status['age'] + '\n')
            screen.printString('Level: ' + self.status['level'] + '\n')
            screen.printString('Gold: ' + self.status['gold'] + '\n\n')
            self.drawBar(screen, w, 'hp', self.vitals['hp'], self.vitals['maxhp'], 41, color)
            self.drawBar(screen, w, 'mp', self.vitals['mp'], self.vitals['maxmp'], 44, color)
            self.drawBar(screen, w, 'ep', self.vitals['ep'], self.vitals['maxep'], 42, color)
            self.drawBar(screen, w, 'wp', self.vitals['wp'], self.vitals['maxwp'], 45, color)
            screen.printString('\n[ Inventory ]\n')
            for key, item in self.inventory.items():
                if 'attrib' in item and not 'w' in item['attrib'] and not 'l' in item['attrib']:
                    if 'icon' in item:
                        screen.printString(self.getIcon(item['icon']) + ' ')
                    screen.printString(self.cutString(item['name'], 35) + '\n')
                    
            screen.printString('\n[ Worn ]\n')
            for key, item in self.inventory.items():
                if 'attrib' in item and ('w' in item['attrib'] or 'l' in item['attrib']):
                    if 'icon' in item:
                        screen.printString(self.getIcon(item['icon']) + ' ')
                    screen.printString(self.cutString(item['name'], 35) + '\n')


    def drawBar(self, screen, width, label, v, maxv, c, color):
        string = (' ' + label + ': ' + v + '/' + maxv).ljust(width-2)
        filled = int(round(float(v) / float(maxv) * float(width)))
        screen.printString('[')
        color.updateColor(1)
        color.updateColor(30)
        color.updateColor(c)
        screen.printString(string[:filled], color.getColor())
        color.updateColor(0)
        color.updateColor(1)
        screen.printString(string[filled:], color.getColor())
        screen.printString(']')

        

    def cutString(self, string, length):
        if len(string)>length:
            return string[:length-3] + '...'
        return string

    def input(self, key, manager):
        pass

    def getIcon(self, icon):
        if icon == "":
            return ""
        if icon in self.icons:
            return self.icons[icon]
        else:
            return '('+icon+')'
