from tkinter import *
from grid import *
from rules import *
from random import randrange

class Application(Tk):
    "Jeu de la vie, exemple d'automates cellulaires"
    def __init__(self, widthGrid=50, heightGrid=50, sideBox=15):
        Tk.__init__(self)
        self.title("Conway's Game of Life")
        # Compteur de cycle
        self.count = 0
        
        # Dessin de la grille où évole les automates cellulaires
        self.widthGrid, self.heightGrid, self.sideBox = widthGrid, heightGrid, sideBox
        self.grille = Grid(self, self.widthGrid, self.heightGrid, self.sideBox)
        self.grille.pack(side=LEFT)

        #Définition des boutons de controle
        Button(self, text='Generate', command=self.genere).pack(fill=X)
        Button(self, text='Clear', command=self.clear).pack(fill=X)
        self.btStart = Button(self, text='Start', command=self.start)
        self.btStart.pack(fill=X)
        self.btNext = Button(self, text='Next', command=self.nextIt)
        self.btNext.pack(fill=X)

        Label(self, text='Style :').pack(fill=X)
        self.choiceColour = StringVar()
        self.choiceColour.set('colorful')
        Radiobutton(self, text='Classic', variable=self.choiceColour, value='classic', command=self.setColour).pack(fill=X)
        Radiobutton(self, text='Colorful', variable=self.choiceColour, value='colorful', command=self.setColour).pack(fill=X)

        self.lbCycle = Label(self, text=self.configTxtCycle())
        self.lbCycle.pack(fill=X)

        # Régler la vitesse
        slider = Scale(self, orient=HORIZONTAL, label='Speed (ms) :', from_=200, to=1000, tickinterval=800, resolution=10, command=self.setSpeed)
        slider.pack(fill=X)
        slider.set(250)
        
        # Menu de chargement
        self.choiceLoad = IntVar()
        menu = Menubutton(self, text='Load')
        menu.pack(fill=X)
        subMenu = Menu(menu)
        subMenu.add_command(label = 'Still lifes :')
        for (v, lab) in [(0, 'Block'),
                         (1, 'Hive'),
                         (2, 'Loaf'),
                         (3, 'Tub'),
                         (4, 'Barge'),
                         (5, 'Long-Barge'),
                         (6, 'Boat'),
                         (7, 'Long-Boat'),
                         (8, 'Ship'),
                         (9, 'Long-Ship'),
                         (10, 'Canoe'),
                         (11, 'Carrier'),
                         (12, 'Integral Sign'),
                         (13, 'Mango'),
                         (14, 'Pond'),
                         (15, 'Snake'),
                         (16, 'Fish-Hook'),
                         (17, 'Eater2')]:
            subMenu.add_radiobutton(label=lab, variable=self.choiceLoad, value=v, command=self.load)
        subMenu.add_separator()
        subMenu.add_command(label = 'Oscillators :')
        for (v, lab) in [(100, 'Blinker'),
                         (101, 'Star'),
                         (102, 'Cross'),
                         (103, 'French Kiss'),
                         (104, 'Clock'),
                         (105, 'Pinwheel'),
                         (106, 'Octagon'),
                         (107, 'Fumarole'),
                         (108, 'Pentoad'),
                         (109, "Kok's galaxy"),
                         (110, 'Pentadecathlon')]:
            subMenu.add_radiobutton(label=lab, variable=self.choiceLoad, value=v, command=self.load)
        menu.configure(menu = subMenu)
        
        Button(self, text='Quit', command=self.destroy).pack(fill=X)

        # Gestion des évènements
        self.grille.bind("<Button-1>", self.mouseDown)

        # Grille non graphique
        self.cells = {} # current
        self.previousCells = {} # previous step
        self.futureCells = {} # next step
        self.states = {} # map des états des cellules

        # Animation on/off
        self.run = False

        #Patterns
        self.stables = [[2, 2, [[(0, 0), (0, 1), (1, 0), (1, 1)]]], # Block
                        [3, 4, [[(0, 1), (0, 2), (1, 0), (1, 3), (2, 1), (2, 2)]], [[(0, 1), (1, 0), (1, 2), (2, 0), (2, 2), (3, 1)]]], # Hive
                        [4, 4, [[(0, 2), (1, 1), (1, 3), (2, 0), (2, 3), (3, 1), (3, 2)], [(0, 1), (0, 2), (1, 0), (1, 3), (2, 1), (2, 3), (3, 2)], [(0, 1), (1, 0), (1, 2), (2, 0), (2, 3), (3, 1), (3, 2)], [(0, 1), (0, 2), (1, 0), (1, 3), (2, 0), (2, 2), (3, 1)]]], # Loaf
                        [3, 3, [[(0, 1), (1, 0), (1, 2), (2, 1)]]], #Tub
                        [4, 4, [[(0, 1), (1, 0), (1, 2), (2, 1), (2, 3), (3, 2)], [(0, 2), (1, 1), (1, 3), (2, 0), (2, 2), (3, 1)]]], # Barge
                        [5, 5, [[(0, 1), (1, 0), (1, 2), (2, 1), (2, 3), (3, 2), (3, 4), (4, 3)], [(0, 3), (1, 2), (1, 4), (2, 1), (2, 3), (3, 0), (3, 2), (4, 1)]]], # Long-Barge
                        [3, 3, [[(0, 0), (0, 1), (1, 0), (1, 2), (2, 1)], [(0, 1), (1, 0), (1, 2), (2, 0), (2, 1)], [(0, 1), (0, 2), (1, 0), (1, 2), (2, 1)], [(0, 1), (1, 0), (1, 2), (2, 1), (2, 2)]]], # Boat
                        [4, 4, [[(0, 0), (0, 1), (1, 0), (1, 2), (2, 1), (2, 3), (3, 2)], [(0, 2), (1, 1), (1, 3), (2, 0), (2, 2), (3, 0), (3, 1)], [(0, 2), (0, 3), (1, 1), (1, 3), (2, 0), (2, 2), (3, 1)], [(0, 1), (1, 0), (1, 2), (2, 1), (2, 3), (3, 2), (3, 3)]]], # Long-Boat
                        [3, 3, [[(0, 0), (0, 1), (1, 0), (1, 2), (2, 1), (2, 2)], [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]]], # Ship
                        [4, 4, [[(0, 0), (0, 1), (1, 0), (1, 2), (2, 1), (2, 3), (3, 2), (3, 3)], [(0, 2), (0, 3), (1, 1), (1, 3), (2, 0), (2, 2), (3, 0), (3, 1)]]], # Long-Ship
                        [5, 5, [[(0, 0), (0, 1), (1, 0), (1, 2), (2, 3), (3, 4), (4, 3), (4, 4)], [(0, 3), (0, 4), (1, 4), (2, 3), (3, 0), (3, 2), (4, 0), (4, 1)], [(0, 3), (0, 4), (1, 2), (1, 4), (2, 1), (3, 0), (4, 0), (4, 1)], [(0, 0), (0, 1), (1, 0), (2, 1), (3, 2), (3, 4), (4, 3), (4, 4)]]], # Canoe
                        [3, 4, [[(0, 0), (0, 1), (1, 0), (1, 3), (2, 2), (2, 3)], [(0, 2), (0, 3), (1, 0), (1, 3), (2, 0), (2, 1)]], [[(0, 0), (0, 1), (1, 0), (2, 2), (3, 1), (3, 2)], [(0, 1), (0, 2), (1, 2), (2, 0), (3, 0), (3, 1)]]], # Carrier
                        [5, 5, [[(0, 3), (0, 4), (1, 4), (2, 1), (2, 2), (2, 3), (3, 0), (4, 0), (4, 1)], [(0, 0), (0, 1), (1, 0), (2, 1), (2, 2), (2, 3), (3, 4), (4, 3), (4, 4)]]], # Integral Sign
                        [5, 4, [[(0, 1), (1, 0), (1, 2), (2, 0), (2, 3), (3, 1), (3, 3), (4, 2)], [(0, 2), (1, 1), (1, 3), (2, 0), (2, 3), (3, 0), (3, 2), (4, 1)]], [[(0, 1), (0, 2), (1, 0), (1, 3), (2, 1), (2, 4), (3, 2), (3, 3)], [(0, 2), (0, 3), (1, 1), (1, 4), (2, 0), (2, 3), (3, 1), (3, 2)]]], # Mango
                        [4, 4, [[(0, 1), (0, 2), (1, 0), (1, 3), (2, 0), (2, 3), (3, 1), (3, 2)]]], # Pond
                        [4, 2, [[(0, 0), (0, 1), (1, 0), (2, 1), (3, 0), (3, 1)], [(0, 0), (0, 1), (1, 1), (2, 0), (3, 0), (3, 1)]], [[(0, 0), (0, 1), (0, 3), (1, 0), (1, 2), (1, 3)], [(0, 0), (0, 2), (0, 3), (1, 0), (1, 1), (1, 3)]]], # Snake
                        [4, 4, [[(0, 0), (0, 1), (1, 0), (2, 1), (2, 2), (2, 3), (3, 3)], [(0, 3), (1, 1), (1, 2), (1, 3), (2, 0), (3, 0), (3, 1)], [(0, 2), (0, 3), (1, 3), (2, 0), (2, 1), (2, 2), (3, 0)], [(0, 0), (1, 0), (1, 1), (1, 2), (2, 3), (3, 2), (3, 3)]]], # Fish-Hook
                        [7, 7, [[(0, 4), (1, 3), (1, 5), (2, 3), (2, 5), (3, 1), (3, 2), (3, 3), (3, 5), (3, 6), (4, 0), (5, 1), (5, 2), (5, 3), (5, 5), (5, 6), (6, 3), (6, 5), (6, 6)], [(0, 3), (0, 5), (0, 6), (1, 1), (1, 2), (1, 3), (1, 5), (1, 6), (2, 0), (3, 1), (3, 2), (3, 3), (3, 5), (3, 6), (4, 3), (4, 5), (5, 3), (5, 5), (6, 4)], [(0, 2), (1, 1), (1, 3), (2, 1), (2, 3), (3, 0), (3, 1), (3, 3), (3, 4), (3, 5), (4, 6), (5, 0), (5, 1), (5, 3), (5, 4), (5, 5), (6, 0), (6, 1), (6, 3)], [(0, 0), (0, 1), (0, 3), (1, 0), (1, 1), (1, 3), (1, 4), (1, 5), (2, 6), (3, 0), (3, 1), (3, 3), (3, 4), (3, 5), (4, 1), (4, 3), (5, 1), (5, 3), (6, 2)]]], # Eater2
                        ]
        self.oscillators = [[1, 3, [(0,0), (0,1), (0,2)]], # Blinker
                            [11, 11, [(0,5), (1,4), (1,5),(1,6), (2,2), (2,3), (2,4), (2,6), (2,7), (2,8), (3,2), (3,8), (4,1), (4,2), (4,8), (4,9), (5,0), (5,1), (5,9), (5,10), (6,1), (6,2), (6,8), (6,9), (7,2), (7,8), (8,2), (8,3), (8,4), (8,6), (8,7), (8,8), (9,4), (9,5), (9,6), (10, 5)]], # Star
                            [8, 8, [(0,2), (0,3), (0,4), (0,5), (1,2), (1,5), (2,0), (2,1), (2,2), (2,5), (2,6), (2,7), (3,0), (3,7), (4,0), (4,7), (5,0), (5,1), (5,2), (5,5), (5,6), (5,7), (6,2), (6,5), (7,2), (7,3), (7,4), (7,5)]], # Cross
                            [9, 10, [(0,9), (1,7), (1,8), (1,9), (2,6), (3,3), (3,4), (3,7), (4,2), (4,7), (5,2), (5,5), (5,6), (6,3), (7,0), (7,1), (7,2), (8,0)]], # French Kiss
                            [12, 12, [(0,4), (0,5), (1,4), (1,5), (3,4), (3,5), (3,6), (3,7), (4,3), (4,8), (4,10), (4,11), (5,3), (5,5), (5,6), (5,8), (5,10), (5,11), (6,0), (6,1), (6,3), (6,4), (6,8), (7,0), (7,1), (7,3), (7,8), (8,4), (8,5), (8,6), (8,7), (10,6), (10,7), (11,6), (11,7)]], # Clock
                            [12, 12, [(0,4), (0,5), (1,4), (1,5), (3,4), (3,5), (3,6), (3,7), (4,3), (4,8), (4,10), (4,11), (5,3), (4,5), (5,6), (5,8), (5,10), (5,11), (6,0), (6,1), (6,3), (6,4), (6,8), (7,0), (7,1), (7,3), (7,8), (8,4), (8,5), (8,6), (8,7), (10,6), (10,7), (11,6), (11,7)]], # Pinwheel
                            [8, 8, [(0,3), (0,4), (1,2), (1,5), (2,1), (2,6), (3,0), (3,7), (4,0), (4,7), (5,1), (5,6), (6,2), (6,5), (7,3), (7,4)]], # Octagon
                            [8, 6, [(0,4), (0,5), (1,1), (1,2), (1,5), (2,1), (2,3), (2,4), (3,0), (4,0), (5,1), (5,3), (5,4), (6,1), (6,2), (6,5), (7,4), (7,5)]], # Fumarole
                            [13, 12, [(0,11), (1,9), (1,10), (1,11), (2,8), (3,8), (3,9), (5,4), (6,4), (6,5), (6,6), (6,7), (7,7), (9,2), (9,3), (10,3), (11,0), (11,1), (11,2), (12,0)]], # Pentoad
                            [9, 9, [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,7), (0,8), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,7), (1,8), (2,7), (2,8), (3,0), (3,1), (3,7), (3,8), (4,0), (4,1), (4,7), (4,8), (5,0), (5,1), (5,7), (5,8), (6,0), (6,1), (7,0), (7,1), (7,3), (7,4), (7,5), (7,6), (7,7), (7,8), (8,0), (8,1), (8,3), (8,4), (8,5), (8,6), (8,7), (8,8)]], # Kok's galaxy
                            [10, 3, [(0,1), (1,1), (2,0), (2,2), (3,1), (4,1), (5,1), (6,1), (7,0), (7,2), (8,1), (9,1)]] # Pentadecathlon 
                            ]
        
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

    def setSpeed(self, speed=250):
        "Réglé la vitesse"
        self.speed = int(speed)

    def anim(self):
        "Animer l'automate"
        speed = int(self.speed/2)
        if self.run:
            self.after(speed, self.nextIt)
            self.after(speed, self.anim)

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
            self.stop()
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
        "Détecte la fin : statique"
        diff = [(x,y) for (x,y) in self.cells if self.cells[(x,y)] != self.futureCells[(x,y)]]
        if not diff:
           return True # Finish
        return False # Not finish

    def load(self):
        self.clear()
        middleX, middleY = int(self.widthGrid/2), int(self.heightGrid/2)
        choice = self.choiceLoad.get()
        if choice >= 0 and choice <= 17:
            patternInfo = self.stables[choice]
            width, height, pattern = patternInfo[0], patternInfo[1], patternInfo[2]
            midWidth, midHeight = int(width/2), int(height/2)
            if width == height:
                length = len(pattern)
                if length == 1:
                    for (x,y) in pattern[0]:
                        self.cells[(x+middleX-midWidth, y+middleY-midHeight)] = True
                elif length == 2:
                    for (x,y) in pattern[0]:
                        self.cells[(x+middleX-width-midWidth, y+middleY-midHeight)] = True
                    for (x,y) in pattern[1]:
                        self.cells[(x+middleX+width-midWidth, y+middleY-midHeight)] = True
                else: # 4 symétries
                    for (x,y) in pattern[0]:
                        self.cells[(x+middleX-width-midWidth, y+middleY-height-midHeight)] = True
                    for (x,y) in pattern[1]:
                        self.cells[(x+middleX+width-midWidth, y+middleY-height-midHeight)] = True
                    for (x,y) in pattern[2]:
                        self.cells[(x+middleX-width-midWidth, y+middleY+height-midHeight)] = True
                    for (x,y) in pattern[3]:
                        self.cells[(x+middleX+width-midWidth, y+middleY+height-midHeight)] = True
            else:
                sub = patternInfo[3]
                len1, len2 = len(pattern), len(sub)
                if len1 == 1 and len2 == 1:
                    for (x,y) in pattern[0]:
                        self.cells[(x+middleX-width-midWidth, y+middleY-midHeight)] = True
                    for (x,y) in sub[0]:
                        self.cells[(x+middleX+width-midHeight, y+middleY-midWidth)] = True
                elif len2 == 2 and len2 == 2:
                    for (x,y) in pattern[0]:
                        self.cells[(x+middleX-width-midWidth, y+middleY-height-midHeight-1)] = True
                    for (x,y) in pattern[1]:
                        self.cells[(x+middleX+width-midWidth, y+middleY-height-midHeight-1)] = True
                    for (x,y) in sub[0]:
                        self.cells[(x+middleX-width-midHeight, y+middleY+height-midWidth+1)] = True
                    for (x,y) in sub[1]:
                        self.cells[(x+middleX+width-midHeight, y+middleY+height-midWidth+1)] = True
        else: # Oscillators
            choice = choice - 100
            if choice < 0 or choice > 10:
                return
            patternInfo = self.oscillators[choice]
            midWidth, midHeight, pattern = int(patternInfo[0]/2), int(patternInfo[1]/2), patternInfo[2]
            for (x,y) in pattern:
                self.cells[(x+middleX-midWidth, y+middleY-midHeight)] = True
        self.start()
    
# Programme de test
if __name__ == '__main__':
    app = Application()
        
