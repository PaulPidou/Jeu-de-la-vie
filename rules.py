class rules(object):
    "Règles du jeu de la vie"
    def isCellAlive(cells, x, y):
        try:
            return cells.get((x,y), False) # Si cells est un dictionnaire
        except: # Si cells est une liste
            if (x,y) in cells:
                return True
            else:
                return False

    def analyseCell(cells, x, y):
        "Analyse les 8 cellules autour de la cellule envoyée"
        cpt = 0
        for x1 in range(-1, 2): # parcours de l'entourage de la cellule
            for y1 in range(-1, 2):
                if rules.isCellAlive(cells, x+x1, y+y1) and (x1 != 0 or y1 != 0):
                    cpt += 1
        return cpt

    def nextState(cells, x, y):
        "Calcule l'état suivant de la cellule"
        lgr = rules.analyseCell(cells, x, y)
        if rules.isCellAlive(cells, x, y):
            if lgr == 2 or lgr == 3:
                return True # vivante
            else:
                return False # morte
        else:
            if lgr == 3:
                return True # vivante
            else:
                return False # morte

    def haveState(currentCells, previousCells, futureCells):
        "Donne l'état des cellules actuel"
        states = {}
        for key, value in currentCells.items():
            if rules.isCellAlive(previousCells, key[0], key[1]) and rules.isCellAlive(currentCells, key[0], key[1]) and rules.isCellAlive(futureCells, key[0], key[1]):
                states[key] = 2 # bleu
            elif rules.isCellAlive(currentCells, key[0], key[1]) and rules.isCellAlive(futureCells, key[0], key[1]):
                states[key] = 1 # vert
            elif rules.isCellAlive(previousCells, key[0], key[1]) and rules.isCellAlive(currentCells, key[0], key[1]):
                states[key] = 3 # rouge
            elif rules.isCellAlive(currentCells, key[0], key[1]):
                states[key] = 4 # jaune
        return states
                
    
