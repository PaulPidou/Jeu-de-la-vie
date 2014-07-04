from tkinter import *
from grid import *
from rules import *
from pattern import *
from random import randrange

class Application(Tk):
    "Jeu de la vie, exemple d'automates cellulaires"
    def __init__(self, widthGrid=50, heightGrid=50, sideBox=15):
        Tk.__init__(self)
        self.title('Jeu de la vie')
        # Compteur de cycle
        self.count = 0
        
        # Dessin de la grille où évole les automates cellulaires
        self.widthGrid, self.heightGrid, self.sideBox = widthGrid, heightGrid, sideBox
        self.grille = Grid(self, self.widthGrid, self.heightGrid, self.sideBox)
        self.grille.pack(side=LEFT)

        #Définition des boutons de controle
        Button(self, text='Générer', command=self.genere).pack(fill=X)
        Button(self, text='Clear', command=self.clear).pack(fill=X)
        self.btStart = Button(self, text='Start', command=self.start)
        self.btStart.pack(fill=X)
        self.btNext = Button(self, text='Next', command=self.nextIt)
        self.btNext.pack(fill=X)

        Label(self, text='Style :').pack(fill=X)
        self.choiceColour = StringVar()
        self.choiceColour.set('colorful')
        Radiobutton(self, text='Classique', variable=self.choiceColour, value='classic', command=self.setColour).pack(fill=X)
        Radiobutton(self, text='Colorée', variable=self.choiceColour, value='colorful', command=self.setColour).pack(fill=X)

        self.lbCycle = Label(self, text=self.configTxtCycle())
        self.lbCycle.pack(fill=X)
        
        Button(self, text='Quitter', command=self.destroy).pack(fill=X)

        # Gestion des évènements
        self.grille.bind("<Button-1>", self.mouseDown)

        # Grille non graphique
        self.cells = {} # current
        self.previousCells = {} # previous step
        self.futureCells = {} # next step
        self.states = {} # map des états des cellules

        # Animation on/off
        self.run = False

        # Détection de pattern
        self.pattern = Pattern(self.widthGrid, self.heightGrid, self.sideBox)

        self.mainloop()

    def configTxtCycle(self):
        "Affiche le nombre de cycle effectué"
        return 'Cycle : ' + str(self.count)

    def checkCells(self):
        "Vérifie si la liste contient quelque chose : True"
        for v in self.cells.values():
            if v:
                return True
        return False

    def setBtNext(self):
        "Rend actif ou inactif le bouton next"
        if self.run:
            self.btNext.configure(state=DISABLED)
        else:
            self.btNext.configure(state=NORMAL)

    def clear(self):
        self.cells.clear()
        self.count = 0
        self.lbCycle.configure(text=self.configTxtCycle())
        self.stop()
        self.grille.clearGrid()

    def genere(self):
        "Remplie une portion de la grille aléatoirement"
        self.cells.clear()
        self.count = 0
        self.lbCycle.configure(text=self.configTxtCycle())
        larg, haut = int(self.widthGrid/2), int(self.heightGrid/2)
        for n in range(larg*haut):
            x, y = randrange(larg), randrange(haut)
            x += int(larg/2)
            y += int(haut/2)
            self.cells[(x,y)] = True # Dictionnaire contenant les positions des cellules vivantes
        self.grille.clearGrid()
        self.grille.drawCells(self.cells)

    def mouseDown(self, event):
        "Action à réaliser au clic gauche de la sourie"
        # Chercher la case visée
        x, y = int(event.x/self.sideBox), int(event.y/self.sideBox)
        if rules.isCellAlive(self.cells, x, y):
            self.cells[(x, y)] = False
        else:
            self.cells[(x, y)] = True
        self.grille.clearGrid()
        self.grille.drawCells(self.cells)

    def anim(self):
        "Animer l'automate"
        if self.run:
            self.after(125, self.nextIt)
            self.after(125, self.anim)

    def start(self):
        "Calcule les prochains cycles en boucle"
        self.run = True
        self.setBtNext()
        self.btStart.configure(text = 'Stop', command=self.stop)
        self.anim()

    def stop(self):
        "Stop le calcul des cycles"
        self.run = False
        self.setBtNext()
        self.btStart.configure(text='Start', command=self.start)

    def nextIt(self):
        "Calcule et affiche le prochain cycle"
        if not self.checkCells(): # Vérigie qu'il y a des données à traiter
            return
        self.count += 1
        self.lbCycle.configure(text=self.configTxtCycle())
        newCells = self.future()
        # on garde en mémoire les états précédents
        self.previousCells.clear()
        self.previousCells = self.cells.copy()
        # on met à jour l'état des cellules
        self.cells.clear()
        self.cells = newCells.copy()
        # on calcule le cycle suivant
        self.futureCells = self.future()
        # on dessine le nouveau état des cellules
        self.setColour()
        self.pattern.detectPattern(self.cells, self.states)
        if self.detectEnd():
            self.stop()

    def future(self):
        "Retourne le cycle suivant"
        newCells = {}
        for x in range(self.widthGrid):
            for y in range(self.heightGrid):
                newCells[(x,y)] = rules.nextState(self.cells,x,y)
        return newCells

    def setColour(self):
        "Colorie les cellulues en fonction du choix du style"
        self.grille.clearGrid()
        self.states = rules.haveState(self.cells, self.previousCells, self.futureCells).copy()
        if self.choiceColour.get() == 'classic':
            self.grille.drawCells(self.cells)
        else:
            self.grille.drawCells(self.cells, self.states)

    def detectEnd(self):
        "Détecte quand les cellules ont atteint un état stable"
        for v in self.states.values():
            if v != 2 and v != 4:
                return False
        return True
    
# Programme de test
if __name__ == '__main__':
    app = Application()
        
