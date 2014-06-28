from tkinter import *
from grid import *
from rules import *
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
        Button(self, text='Quitter', command=self.destroy).pack(fill=X)

        # Grille non graphique
        self.cells = {}

        # Animation on/off
        self.run = False

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
            self.grille.drawCell(x, y)
            self.cells[(x,y)] = True # Dictionnaire contenant les positions des cellules vivantes

    def anim(self):
        "Animer l'automate"
        if self.run:
            self.after(125, self.next)
            self.after(125, self.anim)
        else:
            return

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
        "Calcule le prochain cycle"
        newCells = {}
        for x in range(0, self.widthGrid):
            for y in range(0, self.heightGrid):
                newCells[(x,y)] = rules.nextState(self.cells,x, y)
        self.clearGrid()
        self.cells = newCells.copy()
        self.grille.drawCells(newCells)
        
    
# Programme de test
if __name__ == '__main__':
    app = Application()
        