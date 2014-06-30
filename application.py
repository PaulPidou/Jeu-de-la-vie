from tkinter import *
from grid import *
from rules import *
from pattern import *
from random import randrange

class Application(Tk):
    "Jeu de la vie, exemple d'automates cellulaires"
    def __init__(self):
        Tk.__init__(self)
        self.title('Jeu de la vie')
        
        # Dessin de la grille où évole les automates cellulaires
        self.widthGrid, self.heightGrid, self.sideBox = 50, 50, 15
        self.grille = Grid(self, self.widthGrid, self.heightGrid, self.sideBox)
        self.grille.pack(side=LEFT)

        #Définition des boutons de controle
        Button(self, text='Générer', command=self.genere).pack(fill=X)
        self.btStart = Button(self, text='Start', command=self.start)
        self.btStart.pack(fill=X)
        self.btNext = Button(self, text='Next', command=self.next)
        self.btNext.pack(fill=X)

        Label(self, text='Style :').pack(fill=X)
        self.choiceColour = StringVar()
        self.choiceColour.set('classic')
        Radiobutton(self, text='Classique', variable=self.choiceColour, value='classic', command=self.setColour).pack(fill=X)
        Radiobutton(self, text='Colorée', variable=self.choiceColour, value='colorful', command=self.setColour).pack(fill=X)
        
        Button(self, text='Quitter', command=self.destroy).pack(fill=X)

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

    def setBtNext(self):
        if self.run:
            self.btNext.configure(state=DISABLED)
        else:
            self.btNext.configure(state=NORMAL)

    def clearGrid(self):
        "Redessine la grille à vide"
        self.grille.delete(ALL) # Supprime tout les cellues existantes
        self.cells.clear()
        self.grille.drawGrid() # Redessine la grille

    def genere(self):
        "Remplie une portion de la grille aléatoirement"
        self.clearGrid()
        larg, haut = int(self.widthGrid/2), int(self.heightGrid/2)
        for n in range(larg*haut):
            x, y = randrange(larg), randrange(haut)
            x += int(larg/2)
            y += int(haut/2)
            self.cells[(x,y)] = True # Dictionnaire contenant les positions des cellules vivantes
        self.grille.drawCells(self.cells)

    def anim(self):
        "Animer l'automate"
        if self.run:
            self.after(125, self.next)
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

    def next(self):
        "Calcule et affiche le prochain cycle"
        newCells = self.future()
        # on garde en mémoire les états précédents
        self.previousCells.clear()
        self.previousCells = self.cells.copy()
        # on met à jour l'état des cellules
        self.clearGrid()
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
        self.states = rules.haveState(self.cells, self.previousCells, self.futureCells)
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
        
