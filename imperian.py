# -*- coding: UTF-8 -*-
class World(object):
    def __init__(self):
        self.host = "imperian.com"
        self.port = 23
        self.sidebarWidth = 35
        self.topbarHeight = 15
        self.vitals = {}
        self.items = {}
        self.icons = {
            'humanoid': u'',
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
            #'profile': u'',
            #'rune': u'', #eye sigil enzo
            'curative': u'',
            'monster': u'ﯙ',
            'deadbody': u'ﮊ',
            'food': u'ﴨ',
            'hp': u'',
            'mp': u'',
            'ep': u'',
            'wp': u'',
        }
        self.log = open('world', 'w', 0)

    def onConnect(self, manager):
        manager.sendGMCP('Core.Hello {"Client":"Termud","Version":"0.1"}')
        manager.sendGMCP('Core.Supports.Set ["IRE.Time", "Core 1", "Char 1", "Char.Afflictions 1", "Char.Defences 1", "Char.Items 1", "Char.Skills 1", "Comm.Channel 1", "Room 1", "Redirect 1"]')
        manager.sendGMCP('IRE.Time.Request')

    def onDisconnect(self, manager):
        manager.send('qq')

    def registerWindows(self, manager):
        manager.createWindow("input", "bottom")
        manager.createWindow("status", "bottom")
        manager.createWindow("map", "top", 30)
        manager.createWindow("chat", "top")
        manager.createWindow("item", "side")
        manager.createWindow("main", "fill")
    
    def handleGMCP(self, module, data, manager):
        if module == "Char.Vitals":
            self.vitals.update({'hp': [data['hp'], data['maxhp']]})
            self.vitals.update({'mp': [data['mp'], data['maxmp']]})
            manager.updateWindow("status")

        elif module == "Char.Items.List":
            self.items = {}
            for item in data['items']:
                self.items.update({item['id']: item})
            manager.updateWindow("item")

        elif module == "Char.Items.Add":
            item = data['item']
            self.items.update({item['id']: item})
            manager.updateWindow("item")

        elif module == "Char.Items.Remove":
            item = data['item']
            if item['id'] in self.items:
                del self.items[item['id']]
            manager.updateWindow("item")

        elif module == "Redirect.Window":
            manager.setOutputWindow(data)

        elif module == "Comm.Channel.Start":
            self.previousOutputWindow = manager.getOutputWindow()
            if data != 'say':
                manager.setOutputWindow('chat')

        elif module == "Comm.Channel.End":
            manager.setOutputWindow(self.previousOutputWindow)

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
            colorTracker.restoreColor()

        elif name == "item":
            screen.clear()
            for key, item in self.items.items():
                screen.printString(self.getIcon(item))
                screen.printString(item['name'] + '\n')

    def getIcon(self, item):
        if not 'icon' in item:
            self.log.write(item['name'] + ': none\n')
            return ''
        icon = item['icon']
        if icon in self.icons:
            return self.icons[icon]+' '
        else:
            self.log.write(icon+'\n')
            return icon+'|'


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
