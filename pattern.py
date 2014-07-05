from rules import *

class Pattern(object):
    "Détection et opération sur patterns"
    def __init__(self, width, height, box):
        self.width, self.height, box = width, height, box
        self.cpyCells = {}
        self.cpyStates = {}
        self.currentCycle, self.previousCycle = [], []

    def detectPattern(self, cells, states):
        "Détecte les différents pattern"
        self.cpyCells = cells.copy()
        self.cpyStates = states.copy()
        self.previousCycle = self.currentCycle.copy()
        self.currentCycle = []
        self.detectPatternStable()
        #self.detectPatternOscillating()

    def detectPatternStable(self):
        "Détecte les patterns stable"
        for x in range(self.width):
            for y in range(self.height):
                if rules.isCellAlive(self.cpyCells,x,y) and self.cpyStates[(x,y)] == 2:
                    self.tempStable = []
                    if self.searchNearby(x,y):
                        self.proceedStable()

    def detectPatternOscillating(self):
        "Détecte les patterns oscillants"
        for x in range(self.width):
            for y in range(self.height):
                if rules.isCellAlive(self.cpyCells,x,y):
                    self.tempOscillating = []
                    if self.searchNearbyBis(x,y):
                        self.proceedOscillating()
                    

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
            listStable = self.getPatternStable(pattern)
            self.savePatternStable(listStable)

    def proceedOscillating(self):
        pattern = self.tempOscillating.copy()
        pattern.sort()

        temp = pattern.copy()
        self.count = 0

        if self.futureCells(temp, pattern):
            print('Pattern :', pattern)

        for n in pattern:
            self.cpyCells[n] = False
        

    def futureCells(self, tp, pattern):
        self.count += 1
        temp = tp.copy()
        tp = []
        for x in range(self.width):
            for y in range(self.height):
                if rules.nextState(temp,x,y):
                    tp.append((x,y))
        tp.sort()
        
        if self.comparePattern(tp, pattern): # Pattern oscillant
            return True
        elif not len(tp): # Grille vide
            return False
        elif self.count > 20:
            return False
        else:
            return self.futureCells(tp, pattern)

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

    def comparePattern(self, pattern1, pattern2):
        "Compare deux patterns, renvoie True si identique, False sinon"
        if len(pattern1) != len(pattern2):
            return False
        for i in range(len(pattern1)):
            if pattern1[i] != pattern2[i]:
                return False
        return True

    def compareListPattern(self, pattern, filePattern):
        "Compare le pattern avec les patterns du fichier .txt"
        width, height, widthFile, heightFile = pattern[0], pattern[1], filePattern[0], filePattern[1]
        if not((width == widthFile and height == heightFile) or (width == heightFile and height == widthFile)):
            return False
        if width == widthFile and height == heightFile: # comparer avec premier set
            for n in filePattern[2]:
                if self.comparePattern(pattern[2], n):
                    return True
        else: # comparer avec deuxième set
            for n in filePattern[3]:
                if self.comparePattern(pattern[2], n):
                    return True
        return False

    def savePatternStable(self, pattern):
        "Enregistre les patterns dans un fichier .txt"
        try:
            f = open('patternStable.txt', 'r')
        except:
            print('La sauvegarde des patterns a échoué')
            return
        # Liste qui va accueillir les différents patterns déjà existants
        stringPatterns = f.readlines()
        f.close()
        # On regarde si le nouveau pattern est déjà présent dans la liste
        present = False
        for stringPattern in stringPatterns:
            # Mise en forme : String -> list
            listPattern = self.formatting(stringPattern)
            present = self.compareListPattern(pattern,listPattern)
            if present:
                return
        if not present:
            try:
                f = open('patternStable.txt', 'a')
            except:
                print('La sauvegarde des patterns a échoué')
                return
            patterns = self.searchSymetry(pattern)
            string = str(patterns) + "\n"
            f.write(string)
            f.close()
            print('Found new pattern :', string)

    def detectComma(self, string):
        "Détecte les virgules de premier niveaux et renvoie leur position dans la chaine de caractères"
        cpt1 = cpt2 = 0
        pos = []
        for i in range(len(string)):
            if string[i] == '[':
                cpt1 += 1
            elif string[i] == '(':
                cpt2 += 1
            elif string[i] == ']':
                cpt1 -= 1
            elif string[i] == ')':
                cpt2 -= 1
            elif string[i] == ',' and cpt1 == 1 and cpt2 == 0:
                pos.append(i)
        return pos 

    def formatting(self, string):
        "Met la chaine de caractère reçue en paramètre en forme"
        pos = self.detectComma(string)
        stringPatterns, listPatterns = [], []
        width, height = int(string[1:pos[0]]), int(string[4:pos[1]])
        lgr = len(string)
        if len(pos) == 3: # Présence de deux sets
            stringPatterns.append(string[pos[1]+2:pos[2]])
            stringPatterns.append(string[pos[2]+2:lgr-1])               
        else: # Présence d'un seul set
            stringPatterns.append(string[pos[1]+2:lgr-1])

        for n in stringPatterns:
            listPattern = []
            pos = self.detectComma(n)
            lgr = len(n)
            lgrPos = len(pos)
            if lgrPos == 0: # Une seule liste dans le set
                listPattern.append(self.stringToList(n[1:lgr-2]))
            elif lgrPos == 1: # Deux listes
                listPattern.append(self.stringToList(n[1:pos[0]]))
                listPattern.append(self.stringToList(n[pos[0]+2:lgr-1]))
            elif lgrPos == 2: # Trois listes
                listPattern.append(self.stringToList(n[1:pos[0]]))
                listPattern.append(self.stringToList(n[pos[0]+2:pos[1]]))
                listPattern.append(self.stringToList(n[pos[1]+2:lgr-1]))
            elif lgrPos == 3: # Quatre listes
                listPattern.append(self.stringToList(n[1:pos[0]]))
                listPattern.append(self.stringToList(n[pos[0]+2:pos[1]]))
                listPattern.append(self.stringToList(n[pos[1]+2:pos[2]]))
                listPattern.append(self.stringToList(n[pos[2]+2:lgr-1]))
            else:
                print('Erreur lors de la mise en forme')
            listPatterns.append(listPattern)
        if len(listPatterns) == 2:
            return [width, height, listPatterns[0], listPatterns[1]]
        else:
            return [width, height, listPatterns[0]]

    def stringToList(self, stringList):
        "Convertie une chaine de caractères en liste"
        temp = []
        lgr = len(stringList)
        for n in range(2, lgr, 8):
            x,y = int(stringList[n]), int(stringList[n+3])
            temp.append((x,y))
        return temp

        
