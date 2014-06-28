class rules(object):
    "Règles du jeu de la vie"
    def isCellAlive(cells, x, y):
        return cells.get((x,y), False)

    def analyseCell(cells, x, y):
        cpt = 0
        for x1 in range(-1, 2): # parcours de l'entourgae de la cellule
            for y1 in range(-1, 2):
                if rules.isCellAlive(cells, x+x1, y+y1):
                    cpt += 1
        if cpt > 0 and rules.isCellAlive(cells, x, y):
            cpt -= 1 # évite de comptabilité la cellule analysée
        return cpt

    def nextState(cells, x, y):
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
            
    
