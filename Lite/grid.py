from tkinter import *

class Grid(Canvas):
    "Grille où évoluent les automates cellulaires"
    def __init__(self, boss=None, larg=15, haut=15, box=10):
        Canvas.__init__(self, boss)
        self.configure(width=larg*box, height=haut*box)
        self.larg, self.haut, self.box = larg, haut, box
        # classique / naissante / vivante / mourante / vivante pour un seul cycle
        self.cellState = ['black', 'green', 'blue', 'red', 'yellow'] 
        self.drawGrid()

    def clearGrid(self):
        self.delete(ALL)
        self.drawGrid()

    def drawGrid(self):
        "Dessine la grille"
        x, y = 0, 0
        # lignes d'axe Y
        for n in range(self.larg+1):
            self.create_line(x, 0, x, self.haut*self.box)
            x += self.box
        # lignes d'axe X
        for n in range(self.haut+1):
            self.create_line(0, y, self.larg*self.box, y)
            y += self.box

    def drawCell(self, x, y, state=0):
        "Colorie une cellule"
        self.create_rectangle(x*self.box, y*self.box, (x+1)*self.box, (y+1)*self.box, fill=self.cellState[state])

    def drawCells(self, cells, states=None):
        "Dessines l'ensemble de cellules reçues en paramètre"
        for key, value in cells.items():
            if value:
                x, y = key[0], key[1]
                if states == None:
                    self.drawCell(x, y)
                else:
                    self.drawCell(x, y, states[key])

# Programme de test
if __name__ == '__main__':
    root = Tk()
    gr = Grid(root)
    gr.pack()
    root.mainloop()
