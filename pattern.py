class Pattern(object):
    "Classe créant un pattern vide"
    def __init__(self):
        self.width, self.height = 0, 0
        self.pattern = {} # dictionnaire contenant le dessin d'un patern
        self.possibilities = [] # liste des différentes versions possibles
        self.fixes = [] # points fixe de la figure

    def getPattern(self):
        return self.pattern

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

class Stable(Pattern):
    "Classe créant un patern stable"
    def __init__(self):
        Pattern.__init__(self)

    def resetPattern(self):
        self.width, self.height = 0,0
        self.pattern = {}
        self.fixes = []
        self.possibilities = []

    def createPattern(self, ch=0, simpleListe=True):
        for n in self.fixes:
            self.pattern[n] = True
        if simpleListe:
            if len(self.possibilities):
                try:
                    self.pattern[self.possibilities[ch]] = True
                except:
                    self.pattern[self.possibilities[0]] = True # Dessin par défaut
        else: # liste de listes
            try:
                for sub in self.possibilities[ch]:
                    self.pattern[sub] = True
            except: # Dessin par défaut
                for sub in self.possibilities[0]:
                    self.pattern[sub] = True
            
                

    def createSquare(self):                     ##
        self.resetPattern()                     ##
        self.width = self.height = 2
        self.fixes = [(0,0),(0,1),(1,0),(1,1)]
        self.createPattern()               
        return self.pattern

    def createTube(self):
        self.resetPattern()                     #
        self.width = self.height = 3           # #
        self.fixes = [(1,0),(0,1),(2,1),(1,2)]  #
        self.createPattern()
        return self.pattern

    def createBoat(self, ch=0):
        self.resetPattern()                                 ##  Default
        self.pattern = self.createTube()                    # #
        self.possibilities = [(0,0),(0,2),(2,0),(2,2)]       #
        self.createPattern(ch)
        return self.pattern

    def createShip(self, ch=0):                                 ##  Default
        self.resetPattern()                                     # #
        self.pattern = self.createTube()                         ##
        self.possibilities = [[(0,0),(2,2)],[(0,2),(2,0)]]
        self.createPattern(ch, False)
        return self.pattern

    def createSnake(self, ch=0, orient=0):
        self.resetPattern()
        if orient == 1: # vertical                              ## Vertical default
            self.width, self.height = 2,4                        #                      
            self.fixes = [(0,0),(1,0),(0,3),(1,3)]              #
            self.possibilities = [[(1,1),(0,2)],[(0,1),(1,2)]]  ##

        else: # horizontal                              ## # Horizontal default                                     
            self.width, self.height = 4,2               # ##
            self.fixes = [(0,0),(0,1),(3,0),(3,1)]
            self.possibilities = [[(1,0),(2,1)],[(1,1),(2,0)]]

        self.createPattern(ch, False)
        return self.pattern

    def createBarge(self, orient=0):
        self.resetPattern()
        self.width = self.height = 4
        if orient == 1: # from left to right
            self.fixes = [(1,0),(0,1),(2,1),(1,2),(3,2),(2,3)]
        else:
            self.fixes = [(2,0),(1,1),(3,1),(0,2),(2,2),(1,3)]
        self.createPattern()
        return self.pattern
            
            
        
