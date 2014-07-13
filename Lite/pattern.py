from rules import *

class Pattern(object):
    "Détection et opération sur patterns"
    def __init__(self, width, height, box):
        self.width, self.height, box = width, height, box
        self.cpyCells = {}
        self.cpyStates = {}
        self.listPatternsInPlace, self.listPatternsReplace = [], []
        self.currentCycle, self.previousCycle = [], []

    def clear(self):
        self.listPatternsInPlace, self.listPatternsReplace = [], []

    def existPattern(self, pattern):
        "Véfie l'existence d'un pattern sur la grille"
        for n in pattern:
            if not rules.isCellAlive(self.cpyCells, n[0], n[1]):
                return False
        return True

    def checkIfPatternIsHere(self, pattern):
        "Regarde si le pattern à déjà était traité"
        if not pattern in self.listPatternsInPlace:
            self.listPatternsInPlace.append(pattern)
            return False
        return True

    def detectPattern(self, cells, states):
        "Détecte les différents pattern"
        self.cpyCells = cells.copy()
        self.cpyStates = states.copy()
        self.previousCycle = self.currentCycle.copy()
        self.currentCycle = []
        for pattern in self.listPatternsInPlace:
            if not self.existPattern(pattern):
                self.listPatternsInPlace.remove(pattern)
        self.detectPatternStable()

    def detectPatternStable(self):
        "Détecte les patterns stable"
        for x in range(self.width):
            for y in range(self.height):
                if rules.isCellAlive(self.cpyCells,x,y) and self.cpyStates[(x,y)] == 2:
                    self.tempStable = []
                    if self.searchNearby(x,y):
                        self.proceedStable()

    def searchNearby(self, x, y):
        "Détecte l'entourage"
        self.tempStable.append((x,y))
        for x1 in range(-1, 2): # Parcours de l'entourage de la cellule
            for y1 in range(-1, 2):
                if rules.isCellAlive(self.cpyCells, x+x1, y+y1) and (x1 != 0 or y1 != 0) and not((x+x1,y+y1) in self.tempStable):
                    if self.cpyStates[(x+x1,y+y1)] == 2:
                        if not self.searchNearby(x+x1,y+y1):
                            return False
                    else:
                        return False
        return True

    def searchNearbyBis(self, x, y):
        "Détecte l'entourage"
        self.tempOscillating.append((x,y))
        for x1 in range(-1, 2): # Parcours de l'entourage de la cellule
            for y1 in range(-1, 2):
                if rules.isCellAlive(self.cpyCells, x+x1, y+y1) and (x1 != 0 or y1 != 0) and not((x+x1,y+y1) in self.tempOscillating):
                    self.searchNearbyBis(x+x1,y+y1)
        return True

    def proceedStable(self):
        "Reréférence le pattern et l'enregistre"
        pattern = self.tempStable.copy()
        pattern.sort()
        for n in pattern:
            self.cpyCells[n] = False
        if not pattern in self.previousCycle:
            self.currentCycle.append(pattern)
        else:
            if self.checkIfPatternIsHere(pattern):
                return
            listStable = self.getPatternStable(pattern)
            sym = self.searchSymetry(listStable)
            if not sym in self.listPatternsReplace:
                self.listPatternsReplace.append(sym)
                print('Pattern :', sym, 'found in', pattern[0])

    def getPatternStable(self, data):
        "Reréférence le pattern le renvoie mise en forme"
        maxX = maxY = 0
        minX, minY = self.width, self.height
        for n in data:
            if n[0] > maxX:
                maxX = n[0]
            if n[0] < minX:
                minX = n[0]
            if n[1] > maxY:
                maxY = n[1]
            if n[1] < minY:
                minY = n[1]
        # Afin de trouver la largeur et la hauteur du pattern
        width, height = maxX-minX+1, maxY-minY+1
        # Liste qui va accueillir le pattern reréférencé (0,0)
        pattern = []
        for n in data:
            x, y = n[0]-minX, n[1]-minY
            pattern.append((x,y))
        return [width, height, pattern]

    def comparePattern(self, pattern1, pattern2):
        "Compare deux patterns, renvoie True si identique, False sinon"
        if len(pattern1) != len(pattern2):
            return False
        for i in range(len(pattern1)):
            if pattern1[i] != pattern2[i]:
                return False
        return True

    def searchSymetry(self, dataPattern):
        "Cherche les différentes symétries du pattern"
        if len(dataPattern) != 3:
            print('Mise en forme du pattern non valide')
            return
        width,height,data = dataPattern[0]-1, dataPattern[1]-1,dataPattern[2]
        # liste qui va contenir les symétries trouvées
        symetry = self.getSymetry(width, height,data)
        if width == height: # 3 symétries à réaliser
            return [width+1, height+1, symetry]
        else: # inversement x <-> y
            temp = []
            for n in data:
                x,y = n[1],n[0]
                temp.append((x,y))
            temp.sort()
            symetryBis = self.getSymetry(height,width,temp)
            return [width+1, height+1, symetry, symetryBis]

    def getSymetry(self, width, height, data):
        "Cherche les trois symétries simples du pattern"
        symetry = []
        symetry.append(data)
        temp1, temp2, temp3 = [], [], []
        for n in data:
            x,y = width-n[0], n[1] # symétrie selon un axe vertical
            temp1.append((x,y))
            x,y = n[0], height-n[1] # symétrie selon un axe horizontal
            temp2.append((x,y))
            x,y = width-n[0], height-n[1] # symétrie centrale
            temp3.append((x,y))
        temp1.sort()
        temp2.sort()
        temp3.sort()
        if not self.comparePattern(data, temp1):
            symetry.append(temp1)
        if not self.comparePattern(data, temp2) and not self.comparePattern(temp1, temp2):
            symetry.append(temp2)
        if not self.comparePattern(data, temp3):
            symetry.append(temp3)
        return symetry           
