from rules import *

class Pattern(object):
    "Détection et opération sur patterns"
    def __init__(self, width, height, box):
        self.width, self.height, box = width, height, box
        self.cpyCells = {}
        self.cpyStates = {}
        self.previousCycle = []

    def detectPattern(self, cells, states):
        "Détecte les différents pattern"
        self.cpyCells = cells.copy()
        self.cpyStates = states.copy()
        self.detectPatternStable()

    def detectPatternStable(self):
        "Détecte les patterns stable"
        for x in range(self.width):
            for y in range(self.height):
                if rules.isCellAlive(self.cpyCells,x,y) and self.cpyStates[(x,y)] == 2:
                    self.tempStable = []
                    if self.searchNearby(x,y):
                        self.proceedStable()

    def searchNearby(self, x,y):
        "Détecte l'entourage"
        self.tempStable.append((x,y))
        for x1 in range(-1, 2): # Parcours de l'entourage de la cellule
            for y1 in range(-1, 2):
                if rules.isCellAlive(self.cpyCells, x+x1, y+y1) and (x1 != 0 or y1 != 0) and not(x+x1,y+y1) in self.tempStable:
                    if self.cpyStates[(x+x1,y+y1)] == 2:
                        return self.searchNearby(x+x1,y+y1)
                    else:
                        return False
        return True

    def proceedStable(self):
        self.tempStable.sort()
        for n in self.tempStable:
            self.cpyCells[n] = False
        if not self.tempStable in self.previousCycle:
            self.previousCycle.append(self.tempStable)
        else:
            listStable = self.getPatternStable()
            self.savePatternStable(listStable)

    def getPatternStable(self):
        maxX = maxY = 0
        minX, minY = self.width, self.height
        for n in self.tempStable:
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
        for n in self.tempStable:
            x, y = n[0]-minX, n[1]-minY
            pattern.append((x,y))
        return [width, height, pattern]

    def savePatternStable(self, listPattern):
        try:
            f = open('patternStable.txt', 'r')
        except:
            print('La sauvegarde des patterns a échoué')
            return
        # Liste qui va accueillir les différents patterns déjà existants
        patterns = f.readlines()
        f.close()
        # On regarde si le nouveau pattern est déjà présent dans la liste
        present = False
        for sub in patterns:
            # Mise en forme : String -> list
            lgr = len(sub)-2
            listSub = [int(sub[1]), int(sub[4]), sub[7:lgr]]
            temp = []
            for n in range(2, lgr-7, 8):
                x,y = int(listSub[2][n]), int(listSub[2][n+3])
                temp.append((x,y))
            listSub[2] = temp
            # On vérifie d'abord la correspondance de la largeur et de la longueur
            if listSub[0] == listPattern[0] and listSub[1] == listPattern[1] and len(listSub[2]) == len(listPattern[2]):
                # Puis on vérfie point par point
                for i in range(len(listSub[2])):
                    if listSub[2][i] == listPattern[2][i]:
                        present = True
        if not present:
            try:
                f = open('patternStable.txt', 'a')
            except:
                print('La sauvegarde des patterns a échoué')
                return
            string = str(listPattern) + "\n"
            f.write(string)
            f.close()
                        
            
        
