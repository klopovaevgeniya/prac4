import tools

class tMenu(object):
    def __init__(self, items, lx=0, ty=0, startItem=0):
        self.items = items
        self.curItem = startItem
        self.lx = lx
        self.ty = ty
        self.width = len(max(items, key=len))

    def showCursor(self):
        tools.gotoxy(self.lx,self.ty+self.curItem)
        print("->", end="")

    def hideCursor(self):
        tools.gotoxy(self.lx,self.ty+self.curItem)
        print("  ", end="")

    def nextItem(self):
        self.hideCursor()
        if self.curItem < len(self.items)-1:
            self.curItem +=1
        else:
            self.curItem = 0
        self.showCursor()

    def prevItem(self):
        self.hideCursor()
        if self.curItem > 0:
            self.curItem -=1
        else:
            self.curItem = len(self.items)-1
        self.showCursor()

    def firstItem(self):
        self.hideCursor()
        self.curItem = 0
        self.showCursor()

    def lastItem(self):
        self.hideCursor()
        self.curItem = len(self.items)-1
        self.showCursor()

    def runMenu(self):
        i=0
        tools.hide_cursor()
        for it in self.items:
            tools.gotoxy(self.lx,self.ty+i)
            print(" "*self.width, end="")
            tools.gotoxy(self.lx,self.ty+i)
            print("  "+it+"\n", end="")
            i+=1

        self.showCursor()
        while True:
            key = ord(tools.getch())
            if key == 72:   # KEY_UP
                self.prevItem()
            elif key == 80: # KEY_DOWN
                self.nextItem()
            elif key == 71: # HOME
                self.firstItem()
            elif key == 79: #END
                self.lastItem()
            elif key == 13: #ENTER
                return self.curItem
            elif key == 27: #Escape
                return -27
