import sys
sys.path.insert(0, './src')
from cmath import sqrt
from mimetypes import init
from operator import ipow
import os
import time
import numpy as np
from color import *
from objects import Archer, Balloon, Barbarian, Cannon, Hut, Item, King, Queen, Wall, WizardTower
from objects import Town
# from screen import Screen
from input import input_to
from input import Get
import threading
from playsound import playsound

KEYS = ['a', 'd']
class Screen:
    def __init__(self, height, width):
        self._height = height
        self._width = width
       
        self._board = np.zeros((self._height, self._width), dtype='object')
        for i in range(self._height):
            for j in range(self._width):
                self._board[i][j] = ''

        print("\033[2J")  # CLAERING SCREEN

    def clean(self):
        self._board = np.zeros((self._height, self._width), dtype='object')
        for i in range(self._height):
            for j in range(self._width):
                self._board[i][j] = ''
        # set screen to begining
        print("\033[0;0H")
        i = 0
        while i < self._height:
            j = 0
            while j < self._width:
                print(self._board[i][j], end='')
                j += 1
            print(" ")
            i += 1

    def render_screen(self):
        # set cursor to beginning
        print("\033[0;0H")

        i = 0
        while i < self._height:
            j = 0
            while j < self._width:
                print(self._board[i][j], end='')
                j += 1
            print("")
            i += 1

    def place_object(self, obj):
        print("\033[0;0H")
        pos, size, height, width, maxsize, health_val, damage = obj.get_dimension()
        structure = obj.get_structure()
        health = obj.get_health()
        # print(height,width,pos[0],pos[1],size[0],size[1],maxsize[0],maxsize[1])
        # if(self._board[pos[1]][pos[0]+size[1]]!=' '):
        #     pos[0]=pos[0]-1
        # if(self._board[pos[1]+size[0]][pos[0]]!=' '):
        #     pos[1]=pos[1]-1
        # if(self._board[pos[1]][pos[0]-1]!=' '):
        #     pos[0]=pos[0]+1
        # if(self._board[pos[1]-1][pos[0]]!=' '):
        #     pos[1]=pos[1]+1

        if width == 1:
            if health_val > 0:
                for i in range(pos[1], pos[1]+size[0]):
                    for j in range(pos[0], pos[0]+size[1]):
                        if(self._board[i][j] == ' '):
                            if(health_val > 90):
                                structure[i-pos[1]][j-pos[0]
                                                    ] = bg.green+' '+reset
                            elif (health_val > 50):
                                structure[i-pos[1]][j-pos[0]
                                                    ] = bg.yellow+' '+reset
                            else:
                                structure[i-pos[1]][j-pos[0]
                                                    ] = bg.red+' '+reset

                            self._board[i][j] = structure[i-pos[1]][j-pos[0]]

        else:
            if health_val > 0:
                for i in range(pos[1], pos[1]+size[0]):
                    for j in range(pos[0], pos[0]+size[1]):
                        if(self._board[i][j] == ' '):
                            self._board[i][j] = structure[i-pos[1]][j-pos[0]]
                for i in range(2):
                    for j in range(size[1]):
                        if(health_val > 90):
                            health[i][j] = bg.green+' '+reset
                        elif (health_val > 50):
                            health[i][j] = bg.yellow+' '+reset
                        else:
                            health[i][j] = bg.red+' '+reset
                # pos[1]=pos[1]-2
                for i in range(pos[1], pos[1]+1):
                    for j in range(pos[0], pos[0]+size[1]):
                        self._board[i-2][j] = health[i-pos[1]][j-pos[0]]

    def reset_screen(self):
        # Adjust and start a screen/.,
        self._board = np.array([[' ' for j in range(self._width)]
                               for i in range(self._height)], dtype='object')
        # self._board = np.zeros((self._height, self._width), dtype='object')
        # for i in range(self._height):
        #     for j in range(self._width):
        #         self._board[i][j] = ''
        # Adjust the constant background
        # setup walls
        # for i in range(self._height):
        i = 0
        while i < self._height:
            j = 0
            while j < self._width:
                if(i == 0 or i == self._height-1):
                    self._board[i][j] = bg.green+' '+reset
                # Left and Right Wall
                elif(j == 1 or j == self._width-1):
                    self._board[i][j] = bg.green+' '+reset
                j += 1
            i += 1

    def game_won(self):

        print("\033[2J")  # clear the screen!!
        print("\033[0;0H")
        message = '''
                    YOU WON
                '''

        print("\n\n\n\n\n")
        print(fg.green + message + reset)
        print("\n\n\n\n\n\n")
        sys.exit(0)

    def game_lost(self):
        print("\033[2J")  # clear the screen!!
        print("\033[0;0H")
        message = '''
            YOU LOST 
        '''

        print("\n\n\n")
        print(fg.red + message + reset)
        print("\n\n\n\n\n")
        sys.exit(0)



class Game:
    def __init__(self):
        rows, cols = os.popen('stty size', 'r').read().split()
        rows = int(rows)
        cols = int(cols)
        self.ran = 1
        self._kingval = 0
        self._queenval = 0
        # self._leftx =[int(self._width/2)-6,]
        # self._lefty=[int(self._height/2) - 4,int(self._height/2) - 3,int(self._height/2) - 2,int(self._height/2) - 1,int(self._height/2) ,int(self._height/2)+1,int(self._height/2)+2,int(self._height/2)+3,int(self._height/2)+4]
        # self._rightx=[int(self._height/2) - 4,int(self._height/2) - 3,int(self._height/2) - 2,int(self._height/2) - 1,int(self._height/2) ,int(self._height/2) +1,int(self._height/2) +2,int(self._height/2) +3,int(self._height/2) +4]
        self._kingattack = 1
        self._sword =0
        self._kingattack_falg =0
        self._queenattack_falg =0
        self._queenattack =1
        self._vcounter = 0
        self._v1 = 0
        self._v2 = 0
        
        self._ccounter = 0
        self._c1 = 0
        self._c2 = 0
        
        self._xcounter = 0
        self._x1 = 0
        self._x2 = 0
        
        self._mcounter = 0
        self._a1 = 0
        self._a2 = 0
        
        self._ncounter = 0
        self._n1 = 0
        self._n2 = 0
        
        self._bcounter = 0
        self._b1 = 0
        self._b2 = 0
        
        self._sp1 = 0
        self._sp2 = 0
        self._sp3 = 0
        self._pcounter = 0
        self._sk1 = 0
        self._sk2 = 0
        self._sk3 = 0
        self._kcounter = 0
        self._sl1 = 0
        self._sl2 = 0
        self._sl3 = 0
        self._lcounter = 0
        self._floor = int(0.1*(int(rows)))-4
        self._margin = int(0.4*(int(rows)))
        self._height = int(rows) - self._floor-4
        self._width = int(cols) - self._margin
        self._screen = Screen(self._height, self._width)
        if(rows < 32 or cols < 128):
            print("Increase Terminal Screen Size!!")
            sys.exit(0)
        self._listx = [12, int(
            (self._width/2)), 28, int((self._width-15)), int((self._width/2-15)), 56, 120, 56, 120, int(self._width/2)]
        self._listy = [3, 3, 20, 3, 20, 7, 23, (int(self._height/2))-2]
        self._listh = []

    def start(self):
        self._town = Town([int(self._width/2), (int(self._height/2))-2],
                          [3, 4], int(1), 1, [self._width, self._height], int(100), 0)
        # left wall
        self._wall_left = Wall([int(self._width/2)-3, int(self._height/2) - 5],
                               [1, 1], int(1), int(1), [self._width, self._height], int(100), 0)
        self._wall_left1 = Wall([int(self._width/2)-6, int(self._height/2) - 5+1],
                                [1, 1], int(1), int(1), [self._width, self._height], int(100), 0)
        self._wall_left2 = Wall([int(self._width/2)-6, int(self._height/2) - 3],
                                [1, 1], int(1), int(1), [self._width, self._height], int(100), 0)
        self._wall_left3 = Wall([int(self._width/2)-6, int(self._height/2) - 2],
                                [1, 1], int(1), int(1), [self._width, self._height], int(100), 0)
        self._wall_left4 = Wall([int(self._width/2)-6, int(self._height/2) - 1],
                                [1, 1], int(1), int(1), [self._width, self._height], int(100), 0)
        self._wall_left5 = Wall([int(self._width/2)-6, int(self._height/2)],
                                [1, 1], int(1), int(1), [self._width, self._height], int(100), 0)
        self._wall_left6 = Wall([int(self._width/2)-6, int(self._height/2) + 1],
                                [1, 1], int(1), int(1), [self._width, self._height], int(100), 0)
        self._wall_left7 = Wall([int(self._width/2)-6, int(self._height/2) + 2],
                                [1, 1], int(1), int(1), [self._width, self._height], int(100), 0)
        self._wall_left8 = Wall([int(self._width/2)-6, int(self._height/2) + 3],
                                [1, 1], int(1), int(1), [self._width, self._height], int(100), 0)
        self._wall_left9 = Wall([int(self._width/2)-6, int(self._height/2) + 4],
                                [1, 1], int(1), int(1), [self._width, self._height], int(100), 0)

        self._wall_right = Wall([int(self._width/2)+6+6, int(self._height/2) - 5],
                                [1, 1], int(1), int(1), [self._width, self._height], int(100), 0)

        self._wall_right1 = Wall([int(self._width/2)+6+6, int(self._height/2) - 4], [
                                 1, 1], int(1), int(1), [self._width, self._height], int(100), 0)
        self._wall_right2 = Wall([int(self._width/2)+6+6, int(self._height/2) - 3], [
                                 1, 1], int(1), int(1), [self._width, self._height], int(100), 0)
        self._wall_right3 = Wall([int(self._width/2)+6+6, int(self._height/2) - 2], [
                                 1, 1], int(1), int(1), [self._width, self._height], int(100), 0)
        self._wall_right4 = Wall([int(self._width/2)+6+6, int(self._height/2) - 1], [
                                 1, 1], int(1), int(1), [self._width, self._height], int(100), 0)
        self._wall_right5 = Wall([int(self._width/2)+6+6, int(self._height/2)], [
                                 1, 1], int(1), int(1), [self._width, self._height], int(100), 0)
        self._wall_right6 = Wall([int(self._width/2)+6+6, int(self._height/2) + 1], [
                                 1, 1], int(1), int(1), [self._width, self._height], int(100), 0)
        self._wall_right7 = Wall([int(self._width/2)+6+6, int(self._height/2) + 2], [
                                 1, 1], int(1), int(1), [self._width, self._height], int(100), 0)
        self._wall_right8 = Wall([int(self._width/2)+6+6, int(self._height/2) + 3], [
                                 1, 1], int(1), int(1), [self._width, self._height], int(100), 0)
        self._wall_right9 = Wall([int(self._width/2)+6+6, int(self._height/2) + 4], [
                                 1, 1], int(1), int(1), [self._width, self._height], int(100), 0)

        self._wall_up = Wall([int(self._width/2)-6, int(self._height/2) - 5],
                             [1, 18], int(1), int(1), [self._width, self._height], int(100), 0)

        # self._wall_up1 = Wall([int(self._width/2)-6+2, int(self._height/2) - 5], [1, 1], int(1), int(1), [self._width, self._height], int(100), 0)
        # self._wall_up2 = Wall([int(self._width/2)-6+1, int(self._height/2) - 5], [1, 1], int(1), int(1), [self._width, self._height], int(100), 0)
        # self._wall_up3 = Wall([int(self._width/2)-6, int(self._height/2) - 5], [1, 1], int(1), int(1), [self._width, self._height], int(100), 0)
        # self._wall_up4 = Wall([int(self._width/2)-5, int(self._height/2) - 5], [1, 1], int(1), int(1), [self._width, self._height], int(100), 0)
        # self._wall_up5 = Wall([int(self._width/2)-4, int(self._height/2) - 5], [1, 1], int(1), int(1), [self._width, self._height], int(100), 0)
        # self._wall_up6 = Wall([int(self._width/2)-3, int(self._height/2) - 5], [1, 1], int(1), int(1), [self._width, self._height], int(100), 0)
        # self._wall_up7 = Wall([int(self._width/2)-2, int(self._height/2) - 5], [1, 1], int(1), int(1), [self._width, self._height], int(100), 0)
        # self._wall_up8 = Wall([int(self._width/2)-1, int(self._height/2) - 5], [1, 1], int(1), int(1), [self._width, self._height], int(100), 0)
        # self._wall_up9 = Wall([int(self._width/2), int(self._height/2) - 5], [1, 1], int(1), int(1), [self._width, self._height], int(100), 0)

        self._wall_down = Wall([int(self._width/2)-6, int(self._height/2) - 5+10],   [
                               1, 18], int(1), int(1), [self._width, self._height], int(100), 0)
        self._king = King([int(6), int(self._height/2)], [1, 1],
                          2, 2, [self._width, self._height], int(100), 25)
        self._queen = Queen([int(6), int(self._height/2)], [1, 1],
                          2, 2, [self._width, self._height], int(100), 15)
        
        self._barbarian_p = Barbarian([10, 25], [1, 1], 1, 2, [
                                      self._width, self._height], int(100), 2)
        self._barbarian_p1 = Barbarian([10, 25], [1, 1], 1, 2, [
                                       self._width, self._height], int(100), 1)
        self._barbarian_p2 = Barbarian([10, 25], [1, 1], 1, 2, [
                                       self._width, self._height], int(100), 1)

        self._barbarian_k = Barbarian([25, 10], [1, 1], 1, 2, [
                                      self._width, self._height], int(100), 1)
        self._barbarian_k1 = Barbarian([25, 10], [1, 1], 1, 2, [
                                       self._width, self._height], int(100), 1)
        self._barbarian_k2 = Barbarian([25, 10], [1, 1], 1, 2, [
                                       self._width, self._height], int(100), 1)

        self._barbarian_l = Barbarian([80, 25], [1, 1], 1, 2, [
                                      self._width, self._height], int(100), 1)
        self._barbarian_l1 = Barbarian([80, 25], [1, 1], 1, 2, [
                                       self._width, self._height], int(100), 1)
        self._barbarian_l2 = Barbarian([80, 25], [1, 1], 1, 2, [
                                       self._width, self._height], int(100), 1)

        self._archer1 = Archer([81, 25], [1, 1], 1, 2, [
                                      self._width, self._height], int(50), 1)
        self._archer2 = Archer([81, 25], [1, 1], 1, 2, [
                                      self._width, self._height], int(50), 1)
        self._narcher1 = Archer([11, 25], [1, 1], 1, 2, [
                                      self._width, self._height], int(50), 1)
        self._narcher2 = Archer([11, 25], [1, 1], 1, 2, [
                                      self._width, self._height], int(50), 1)
        self._barcher1 = Archer([28, 25], [1, 1], 1, 2, [
                                      self._width, self._height], int(50), 1)
        self._barcher2 = Archer([28, 25], [1, 1], 1, 2, [
                                      self._width, self._height], int(50), 1)
        #ballons
        self._Balloon1 = Balloon([81, 29], [1, 1], 1, 2, [
                                      self._width, self._height], int(50), 1)
        self._Balloon2 = Balloon([81, 29], [1, 1], 1, 2, [
                                      self._width, self._height], int(50), 1)
        self._cBalloon1 = Balloon([11, 29], [1, 1], 1, 2, [
                                   self._width, self._height], int(50), 1)
        self._cBalloon2 = Balloon([11, 29], [1, 1], 1, 2, [
                                      self._width, self._height], int(50), 1)
        self._xBalloon1 = Balloon([28, 29], [1, 1], 1, 2, [
                                      self._width, self._height], int(50), 1)
        self._xBalloon2 = Balloon([28, 29], [1, 1], 1, 2, [
                                      self._width, self._height], int(50), 1)
        
        self._hut1 = Hut([int(12), int(3)], [1, 1], 1, 1, [
                         self._width, self._height], int(100), 0)
        self._hut2 = Hut([int((self._width/2)), int(3)], [1, 1],
                         1, 1, [self._width, self._height], int(100), 0)
        self._hut3 = Hut([int(28), int(20)], [1, 1], 1, 1, [
                         self._width, self._height], int(100), 0)
        self._hut4 = Hut([int((self._width-15)), int(3)], [1, 1],
                         1, 1, [self._width, self._height], int(100), 0)
        self._hut5 = Hut([int((self._width-15)), int(20)], [1, 1],
                         1, 1, [self._width, self._height], int(100), 0)
        
        self._qhut1 = Hut([int(35), int(12)], [1, 1], 1, 1, [
                         self._width, self._height], int(100), 0)
        self._qhut2 = Hut([int(37), int(14)], [1, 1],
                         1, 1, [self._width, self._height], int(100), 0)
        self._qhut3 = Hut([int(39), int(12)], [1, 1], 1, 1, [
                         self._width, self._height], int(100), 0)
        
        
        self._cannon1 = Cannon([int(56), int(7)], [1, 1], 1, 0, [
                               self._width, self._height], int(100), 5)
        self._cannon2 = Cannon([int(120), int(23)], [1, 1], 1, 0, [
                               self._width, self._height], int(100), 5)
        self._wizard1 = WizardTower([int(130), int(7)], [1, 1], 1, 0, [
                               self._width, self._height], int(100), 10)
        self._wizard2 = WizardTower([int(40), int(23)], [1, 1], 1, 0, [
                               self._width, self._height], int(100), 10)
        self._listx = [12, int((self._width/2)), 28, int((self._width-15)),
                               int((self._width-15)), 56, 120, 56, 120, int(self._width/2)]
        self._listy = [3, 3, 20, 3, 20, 7, 23, (int(self._height/2))-2]
        self._prix = [130,40, 56, 120]
        self._priy = [7,23,7, 23,]
        
    def wizard_attack(self):
        pos, size, height, width, maxsize, health_val, damage = self._wizard1.get_dimension()
        pos1, size1, height1, width1, maxsize1, health_val1, damage1 = self._wizard2.get_dimension()
        kinghealth = self._king.get_health()
        kingpos = self._king.item_pos()
        count = 0
        p1 = self._Balloon1.item_pos()
        p2 = self._Balloon2.item_pos()
        p3 = self._cBalloon1.item_pos()
        j1 = self._cBalloon2.item_pos()
        j2 = self._xBalloon1.item_pos()
        j3 = self._xBalloon2.item_pos()
        l1 = self._barbarian_l.item_pos()
        l2 = self._barbarian_l1.item_pos()
        l3 = self._barbarian_l2.item_pos()

        print(health_val1,self._cBalloon1._health_val, self._c1,self._c2,"here")
        if(kingpos[0] >= (health_val > 0 and pos[0]-5) and (kingpos[0] <= (pos[0]+5)) and (kingpos[1] >= (pos[1]-5)) and (kingpos[1] <= (pos[1]+5))) or ((health_val1 > 0 and kingpos[0] >= (pos1[0]-5) and (kingpos[0] <= (pos1[0]+5)) and (kingpos[1] >= (pos1[1]-5)) and (kingpos[1] <= (pos1[1]+5)))):
            self._king.update_health(damage)
            threading.Thread(target=playsound, args=('./resources/moving.mp3',), daemon=True).start()
            
        if(self._v1 == 1 and ((health_val > 0 and p1[0] >= (pos[0]-5) and (p1[0] <= (pos[0]+5)) and (p1[1] >= (pos[1]-5)) and (p1[1] <= (pos[1]+5))) or ((health_val1 > 0 and p1[0] >= (pos1[0]-5) and (p1[0] <= (pos1[0]+5)) and (p1[1] >= (pos1[1]-5)) and (p1[1] <= (pos1[1]+5)))))):
            self._Balloon1.update_health(damage)
            threading.Thread(target=playsound, args=('./resources/moving.mp3',), daemon=True).start()

        if(self._v2 == 1 and ((health_val > 0 and p2[0] >= (pos[0]-5) and (p2[0] <= (pos[0]+5)) and (p2[1] >= (pos[1]-5)) and (p2[1] <= (pos[1]+5))) or ((health_val1 > 0 and p2[0] >= (pos1[0]-5) and (p2[0] <= (pos1[0]+5)) and (p2[1] >= (pos1[1]-5)) and (p2[1] <= (pos1[1]+5)))))):
            self._Balloon2.update_health(damage)
            threading.Thread(target=playsound, args=('./resources/moving.mp3',), daemon=True).start()
            

        if(self._c1 == 1 and ((health_val > 0 and p3[0] >= (pos[0]-5) and (p3[0] <= (pos[0]+5)) and (p3[1] >= (pos[1]-5)) and (p3[1] <= (pos[1]+5))) or ((health_val1 > 0 and p3[0] >= (pos1[0]-5) and (p3[0] <= (pos1[0]+5)) and (p3[1] >= (pos1[1]-5)) and (p3[1] <= (pos1[1]+5)))))):
            self._cBalloon1.update_health(damage)
            threading.Thread(target=playsound, args=('./resources/moving.mp3',), daemon=True).start()
            

        if(self._c2 == 1 and ((health_val > 0 and j1[0] >= (pos[0]-5) and (j1[0] <= (pos[0]+5)) and (j1[1] >= (pos[1]-5)) and (j1[1] <= (pos[1]+5))) or ((health_val1 > 0 and j1[0] >= (pos1[0]-5) and (j1[0] <= (pos1[0]+5)) and (j1[1] >= (pos1[1]-5)) and (j1[1] <= (pos1[1]+5)))))):
            self._cBalloon2.update_health(damage)
            threading.Thread(target=playsound, args=('./resources/moving.mp3',), daemon=True).start()
            

        if(self._x1 == 1 and ((health_val > 0 and j2[0] >= (pos[0]-5) and (j2[0] <= (pos[0]+5)) and (j2[1] >= (pos[1]-5)) and (j2[1] <= (pos[1]+5))) or ((health_val1 > 0 and j2[0] >= (pos1[0]-5) and (j2[0] <= (pos1[0]+5)) and (j2[1] >= (pos1[1]-5)) and (j2[1] <= (pos1[1]+5)))))):
            self._xBalloon1.update_health(damage)
            threading.Thread(target=playsound, args=('./resources/moving.mp3',), daemon=True).start()
            

        if(self._x2 == 1 and ((j3[0] >= (pos[0]-5) and (j3[0] <= (pos[0]+5)) and (j3[1] >= (pos[1]-5)) and (j3[1] <= (pos[1]+5))) or ((j3[0] >= (pos1[0]-5) and (health_val1 > 0 and j3[0] <= (pos1[0]+5)) and (j3[1] >= (pos1[1]-5)) and (j3[1] <= (pos1[1]+5)))))):
            self._xBalloon2.update_health(damage)
            threading.Thread(target=playsound, args=('./resources/moving.mp3',), daemon=True).start()
            

        if(self._sl1 == 1 and ((health_val > 0 and l1[0] >= (pos[0]-5) and (l1[0] <= (pos[0]+5)) and (l1[1] >= (pos[1]-5)) and (l1[1] <= (pos[1]+5))) or ((health_val1 > 0 and l1[0] >= (pos1[0]-5) and (l1[0] <= (pos1[0]+5)) and (l1[1] >= (pos1[1]-5)) and (l1[1] <= (pos1[1]+5)))))):
            self._barbarian_l.update_health(damage)
            threading.Thread(target=playsound, args=('./resources/moving.mp3',), daemon=True).start()

        if(self._sl2 == 1 and ((health_val > 0 and l2[0] >= (pos[0]-5) and (l2[0] <= (pos[0]+5)) and (l2[1] >= (pos[1]-5)) and (l2[1] <= (pos[1]+5))) or ((health_val1 > 0 and l2[0] >= (pos1[0]-5) and (l2[0] <= (pos1[0]+5)) and (l2[1] >= (pos1[1]-5)) and (l2[1] <= (pos1[1]+5)))))):
            self._barbarian_l1.update_health(damage)
            threading.Thread(target=playsound, args=('./resources/moving.mp3',), daemon=True).start()
            

        if(self._sl3 == 1 and ((health_val > 0 and l3[0] >= (pos[0]-5) and (l3[0] <= (pos[0]+5)) and (l3[1] >= (pos[1]-5)) and (l3[1] <= (pos[1]+5))) or ((health_val1 > 0 and l3[0] >= (pos1[0]-5) and (l3[0] <= (pos1[0]+5)) and (l3[1] >= (pos1[1]-5)) and (l3[1] <= (pos1[1]+5)))))):
            self._barbarian_l2.update_health(damage)
            threading.Thread(target=playsound, args=('./resources/moving.mp3',), daemon=True).start()
            

    def cannon_attack(self):
        pos, size, height, width, maxsize, health_val, damage = self._cannon1.get_dimension()
        pos1, size1, height1, width1, maxsize1, health_val1, damage1 = self._cannon2.get_dimension()
        kinghealth = self._king.get_health()
        kingpos = self._king.item_pos()
        count = 0
        p1 = self._barbarian_p.item_pos()
        p2 = self._barbarian_p1.item_pos()
        p3 = self._barbarian_p2.item_pos()
        j1 = self._barbarian_k.item_pos()
        j2 = self._barbarian_k1.item_pos()
        j3 = self._xBalloon2.item_pos()
        l1 = self._barbarian_l.item_pos()
        l2 = self._barbarian_l1.item_pos()
        l3 = self._barbarian_l2.item_pos()

        # print(kingpos[0], kingpos[1], pos[1], pos[0],"here")
        if(kingpos[0] >= (health_val > 0 and pos[0]-5) and (kingpos[0] <= (pos[0]+5)) and (kingpos[1] >= (pos[1]-5)) and (kingpos[1] <= (pos[1]+5))) or ((health_val1 > 0 and kingpos[0] >= (pos1[0]-5) and (kingpos[0] <= (pos1[0]+5)) and (kingpos[1] >= (pos1[1]-5)) and (kingpos[1] <= (pos1[1]+5)))):
            self._king.update_health(damage)
            threading.Thread(target=playsound, args=('./resources/moving.mp3',), daemon=True).start()
            
        elif(self._sp1 == 1 and ((health_val > 0 and p1[0] >= (pos[0]-5) and (p1[0] <= (pos[0]+5)) and (p1[1] >= (pos[1]-5)) and (p1[1] <= (pos[1]+5))) or ((health_val1 > 0 and p1[0] >= (pos1[0]-5) and (p1[0] <= (pos1[0]+5)) and (p1[1] >= (pos1[1]-5)) and (p1[1] <= (pos1[1]+5)))))):
            self._barbarian_p.update_health(damage)
            threading.Thread(target=playsound, args=('./resources/moving.mp3',), daemon=True).start()

        elif(self._sp2 == 1 and ((health_val > 0 and p2[0] >= (pos[0]-5) and (p2[0] <= (pos[0]+5)) and (p2[1] >= (pos[1]-5)) and (p2[1] <= (pos[1]+5))) or ((health_val1 > 0 and p2[0] >= (pos1[0]-5) and (p2[0] <= (pos1[0]+5)) and (p2[1] >= (pos1[1]-5)) and (p2[1] <= (pos1[1]+5)))))):
            self._barbarian_p1.update_health(damage)
            threading.Thread(target=playsound, args=('./resources/moving.mp3',), daemon=True).start()
            

        elif(self._sp3 == 1 and ((health_val > 0 and p3[0] >= (pos[0]-5) and (p3[0] <= (pos[0]+5)) and (p3[1] >= (pos[1]-5)) and (p3[1] <= (pos[1]+5))) or ((health_val1 > 0 and p3[0] >= (pos1[0]-5) and (p3[0] <= (pos1[0]+5)) and (p3[1] >= (pos1[1]-5)) and (p3[1] <= (pos1[1]+5)))))):
            self._barbarian_p2.update_health(damage)
            threading.Thread(target=playsound, args=('./resources/moving.mp3',), daemon=True).start()
            

        elif(self._sk1 == 1 and ((health_val > 0 and j1[0] >= (pos[0]-5) and (j1[0] <= (pos[0]+5)) and (j1[1] >= (pos[1]-5)) and (j1[1] <= (pos[1]+5))) or ((health_val1 > 0 and j1[0] >= (pos1[0]-5) and (j1[0] <= (pos1[0]+5)) and (j1[1] >= (pos1[1]-5)) and (j1[1] <= (pos1[1]+5)))))):
            self._barbarian_k.update_health(damage)
            threading.Thread(target=playsound, args=('./resources/moving.mp3',), daemon=True).start()
            

        elif(self._sk2 == 1 and ((health_val > 0 and j2[0] >= (pos[0]-5) and (j2[0] <= (pos[0]+5)) and (j2[1] >= (pos[1]-5)) and (j2[1] <= (pos[1]+5))) or ((health_val1 > 0 and j2[0] >= (pos1[0]-5) and (j2[0] <= (pos1[0]+5)) and (j2[1] >= (pos1[1]-5)) and (j2[1] <= (pos1[1]+5)))))):
            self._barbarian_k1.update_health(damage)
            threading.Thread(target=playsound, args=('./resources/moving.mp3',), daemon=True).start()
            

        elif(self._sk3 == 1 and ((j3[0] >= (pos[0]-5) and (j3[0] <= (pos[0]+5)) and (j3[1] >= (pos[1]-5)) and (j3[1] <= (pos[1]+5))) or ((j3[0] >= (pos1[0]-5) and (health_val1 > 0 and j3[0] <= (pos1[0]+5)) and (j3[1] >= (pos1[1]-5)) and (j3[1] <= (pos1[1]+5)))))):
            self._barbarian_k2.update_health(damage)
            threading.Thread(target=playsound, args=('./resources/moving.mp3',), daemon=True).start()
            

        elif(self._sl1 == 1 and ((health_val > 0 and l1[0] >= (pos[0]-5) and (l1[0] <= (pos[0]+5)) and (l1[1] >= (pos[1]-5)) and (l1[1] <= (pos[1]+5))) or ((health_val1 > 0 and l1[0] >= (pos1[0]-5) and (l1[0] <= (pos1[0]+5)) and (l1[1] >= (pos1[1]-5)) and (l1[1] <= (pos1[1]+5)))))):
            self._barbarian_l.update_health(damage)
            threading.Thread(target=playsound, args=('./resources/moving.mp3',), daemon=True).start()

        elif(self._sl2 == 1 and ((health_val > 0 and l2[0] >= (pos[0]-5) and (l2[0] <= (pos[0]+5)) and (l2[1] >= (pos[1]-5)) and (l2[1] <= (pos[1]+5))) or ((health_val1 > 0 and l2[0] >= (pos1[0]-5) and (l2[0] <= (pos1[0]+5)) and (l2[1] >= (pos1[1]-5)) and (l2[1] <= (pos1[1]+5)))))):
            self._barbarian_l1.update_health(damage)
            threading.Thread(target=playsound, args=('./resources/moving.mp3',), daemon=True).start()
            

        elif(self._sl3 == 1 and ((health_val > 0 and l3[0] >= (pos[0]-5) and (l3[0] <= (pos[0]+5)) and (l3[1] >= (pos[1]-5)) and (l3[1] <= (pos[1]+5))) or ((health_val1 > 0 and l3[0] >= (pos1[0]-5) and (l3[0] <= (pos1[0]+5)) and (l3[1] >= (pos1[1]-5)) and (l3[1] <= (pos1[1]+5)))))):
            self._barbarian_l2.update_health(damage)
            threading.Thread(target=playsound, args=('./resources/moving.mp3',), daemon=True).start()
            

    def placing(self):
        self._screen.place_object(self._town)
        # self._screen.place_object(self._wall_left)
        self._screen.place_object(self._wall_left1)
        self._screen.place_object(self._wall_left2)
        self._screen.place_object(self._wall_left3)
        self._screen.place_object(self._wall_left4)
        self._screen.place_object(self._wall_left5)
        self._screen.place_object(self._wall_left6)
        self._screen.place_object(self._wall_left7)
        self._screen.place_object(self._wall_left8)
        self._screen.place_object(self._wall_left9)

        # self._screen.place_object(self._wall_right)
        self._screen.place_object(self._wall_right1)
        self._screen.place_object(self._wall_right2)
        self._screen.place_object(self._wall_right3)
        self._screen.place_object(self._wall_right4)
        self._screen.place_object(self._wall_right5)
        self._screen.place_object(self._wall_right6)
        self._screen.place_object(self._wall_right7)
        self._screen.place_object(self._wall_right8)
        self._screen.place_object(self._wall_right9)

        self._screen.place_object(self._wall_up)
        # self._screen.place_object(self._wall_up1)
        # self._screen.place_object(self._wall_up2)
        # self._screen.place_object(self._wall_up3)
        # self._screen.place_object(self._wall_up4)
        # self._screen.place_object(self._wall_up5)
        # self._screen.place_object(self._wall_up6)
        # self._screen.place_object(self._wall_up7)
        # self._screen.place_object(self._wall_up8)
        # self._screen.place_object(self._wall_up9)

        self._screen.place_object(self._wall_down)
        self._screen.place_object(self._hut1)
        self._screen.place_object(self._hut2)
        self._screen.place_object(self._hut4)
        self._screen.place_object(self._hut3)

        self._screen.place_object(self._qhut1)
        self._screen.place_object(self._qhut2)
        self._screen.place_object(self._qhut3)
        
        self._screen.place_object(self._hut5)
        self._screen.place_object(self._cannon1)
        self._screen.place_object(self._cannon2)
        print(self._wizard1._health_val)
        if(self._wizard1._health_val > 0):
            self._screen.place_object(self._wizard1)
        if(self._wizard2._health_val > 0):
            self._screen.place_object(self._wizard2)
        

        if(self._kingval == 1):
            self._screen.place_object(self._king)
            
        if(self._queenval == 1):
            self._screen.place_object(self._queen)
            
        # m counter archer
        if(self._mcounter == 1 and self._a1 == 0):
            self._a1 = 1
        if(self._a1 == 1):
            self._screen.place_object(self._archer1)
            self.archer_attackm1()
        if(self._mcounter == 2 and self._a2 == 0):
            self._a2 = 1
        if(self._a2 == 1):
            self._screen.place_object(self._archer2)
            self.archer_attackm2()
        
        if(self._archer2._health_val <= 0):
            self._a2 = -1
        if(self._archer1._health_val <= 0):
            self._a1 = -1
            
        # n counter
        if(self._ncounter == 1 and self._n1 == 0):
            self._n1 = 1
        if(self._n1 == 1):
            self._screen.place_object(self._narcher1)
            self.archer_nattackm1()
        if(self._ncounter == 2 and self._n2 == 0):
            self._n2 = 1
        if(self._n2 == 1):
            self._screen.place_object(self._narcher2)
            self.archer_nattackm2()
        
        if(self._narcher2._health_val <= 0):
            self._n2 = -1
        if(self._narcher1._health_val <= 0):
            self._n1 = -1
            
        # b counter
        
        if(self._bcounter == 1 and self._b1 == 0):
            self._b1 = 1
        if(self._b1 == 1):
            self._screen.place_object(self._barcher1)
            self.archer_battackm1()
        if(self._bcounter == 2 and self._b2 == 0):
            self._b2 = 1
        if(self._b2 == 1):
            self._screen.place_object(self._barcher2)
            self.archer_battackm2()
        
        if(self._barcher2._health_val <= 0):
            self._b2 = -1
        if(self._barcher1._health_val <= 0):
            self._b1 = -1
        
        if(self._pcounter == 1 and self._sp1 == 0):
            self._sp1 = 1
        if(self._sp1 == 1):
            self._screen.place_object(self._barbarian_p)
            self.barbarian_attackp1()
        
        # v counter archer
        if(self._vcounter == 1 and self._v1 == 0):
            self._v1= 1
        if(self._v1== 1):
            self._screen.place_object(self._Balloon1)
            self.Balloon_attack()
        if(self._vcounter == 2 and self._v2 == 0):
            self._v2 = 1
        if(self._v2 == 1):
            self._screen.place_object(self._Balloon2)
            self.Balloon_attack1()
        
        if(self._Balloon2._health_val <= 0):
            self._v2 = 0
        if(self._Balloon1._health_val <= 0):
            self._v1 = 0
        # c counter
        if(self._ccounter == 1 and self._c1 == 0):
            self._c1 = 1
        if(self._c1 == 1):
            self._screen.place_object(self._cBalloon1)
            self.Balloon_attackc()
        if(self._ccounter == 2 and self._c2 == 0):
            self._c2 = 1
        if(self._c2 == 1):
            self._screen.place_object(self._cBalloon2)
            self.Balloon_attackc1()
        
        if(self._cBalloon1._health_val <= 0):
            self._c1 = 0
        if(self._cBalloon2._health_val <= 0):
            self._c2 = 0
            
        # x counter
        
        if(self._xcounter == 1 and self._x1 == 0):
            self._x1 = 1
        if(self._x1 == 1):
            self._screen.place_object(self._xBalloon1)
            self.Balloon_attackx()
        if(self._xcounter == 2 and self._x2 == 0):
            self._x2 = 1
        if(self._x2 == 1):
            self._screen.place_object(self._xBalloon2)
            self.Balloon_attackx1()
        
        
        
        if(self._xBalloon1._health_val <= 0):
            self._c1= -1
        if(self._xBalloon2._health_val <= 0):
            self._c2 = -1
        
        if(self._pcounter == 1 and self._sp1 == 0):
            self._sp1 = 1
        if(self._sp1 == 1):
            self._screen.place_object(self._barbarian_p)
            self.barbarian_attackp1()
            
            
        if(self._barbarian_p._health_val <= 0):
            self._sp1 = -1
        if(self._barbarian_p1._health_val <= 0):
            self._sp2 = -1
        if(self._barbarian_p2._health_val <= 0):
            self._sp3 = -1
        if(self._pcounter == 2 and self._sp2 == 0):
            self._sp2 = 1

        if(self._sp2 == 1):
            self._screen.place_object(self._barbarian_p1)
            self.barbarian_attackp2()
        if(self._pcounter == 3 and self._sp3 == 0):
            self._sp3 = 1
        if(self._sp3 == 1):
            self._screen.place_object(self._barbarian_p2)
            self.barbarian_attackp3()
           # k counter
           
        if(self._barbarian_k._health_val <= 0):
            self._sk1 = -1
        if(self._barbarian_k1._health_val <= 0):
            self._sk2 = -1
        if(self._barbarian_k2._health_val <= 0):
            self._sk3 = -1
            
        if(self._kcounter == 1 and self._sk1==0):
            self._sk1 = 1
        if(self._sk1 == 1):
            self._screen.place_object(self._barbarian_k)
            self.barbarian_attackj1()
        if(self._kcounter == 2 and self._sk2==0):
            self._sk2 = 1

        if(self._sk2 == 1):
            self._screen.place_object(self._barbarian_k1)
            self.barbarian_attackj2()
        if(self._kcounter == 3):
            self._sk3 = 1
        if(self._sk3 == 1 and self._sk3==0):
            self._screen.place_object(self._barbarian_k2)
            self.barbarian_attackj3()

         # L counter
        if(self._barbarian_l._health_val <= 0):
            self._sl1 = -1
        if(self._barbarian_l1._health_val <= 0):
            self._sl2 = -1
        if(self._barbarian_l2._health_val <= 0):
            self._sl3 = -1
            
        if(self._lcounter == 1 and self._sl1==0):
            self._sl1 = 1
        if(self._sl1 == 1):
            self._screen.place_object(self._barbarian_l)
            self.barbarian_attackl1()
        if(self._lcounter == 2 and self._sl2==0):
            self._sl2 = 1

        if(self._sl2 == 1):
            self._screen.place_object(self._barbarian_l1)
            self.barbarian_attackl2()
        if(self._lcounter == 3 and self._sl3==0):
            self._sl3 = 1
        if(self._sl3 == 1):
            self._screen.place_object(self._barbarian_l2)
            self.barbarian_attackl3()
            
        if(self._kingattack_falg==1):
            self._kingattack = 0
        if(self._queenattack_falg==1):
            self._queenattack = 0
        if(self._sword==1):
            self.king_sword_attck() 
    def king_attack(self):
        pos, size, height, width, maxsize, health_val, damage = self._king.get_dimension()

        # print(self._kingattack_falg, "king attack val:",self._kingattack)
        # print(pos[0],pos[1],"width/2:",int(self._width/2),"height/2:",int(self._height/2),"kingattack:",self._kingattack)
        # print("waal1 :",self._wall_left1)
        if(health_val >0):
            if((self._kingattack == 0) and (pos[0]+1 == int(self._width/2)) and ((pos[1] == int(self._height/2 - 2)) or (pos[1] == int(self._height/2 - 1)) or (pos[1] == int(self._height/2)) or (pos[1] == int(self._height/2 + 1)))):
                self._town.update_health(damage)
            else:
                self._kingattack = 1
            if((self._kingattack == 0) and (pos[0]-1-3 == int(self._width/2)) and ((pos[1] == int(self._height/2 - 2)) or (pos[1] == int(self._height/2 - 1)) or (pos[1] == int(self._height/2)) or (pos[1] == int(self._height/2 + 1)))):
                self._town.update_health(damage)
            else:
                self._kingattack = 1

            if((self._kingattack == 0) and (pos[1]+3 == int(self._height/2 - 2)) and ((pos[0] == int(self._width/2)) or (pos[0] == int(self._width/2)) or (pos[0]+1 == int(self._width/2)) or (pos[0]+2 == int(self._width/2)) or (pos[0]+3 == int(self._width/2)))):
                self._town.update_health(damage)
            else:
                self._kingattack = 1
            if((self._kingattack == 0) and (pos[1]-4 == int(self._height/2 - 2)) and ((pos[0] == int(self._width/2)) or (pos[0]+3 == int(self._width/2)) or (pos[0]+4 == int(self._width/2)) or (pos[0]+2 == int(self._width/2)) or (pos[0]+1 == int(self._width/2)))):
                self._town.update_health(damage)
            else:
                self._kingattack = 1

                # huts
            if((self._kingattack == 1) and (((pos[0]+1 == 12) and pos[1] == 3) or (pos[0]-2 == 12 and pos[1] == 3) or (pos[1]+2 == 3 and pos[0] == 12) or (pos[1]-2 == 3 and pos[0] == 12))):
                self._hut1.update_health(damage)
            else:
                self._kingattack = 1
            if((self._kingattack == 1) and (((pos[0]+1 == int((self._width/2))) and pos[1] == 3) or (pos[0]-2 == int((self._width/2)) and pos[1] == 3) or (pos[1]+2 == 3 and pos[0] == int((self._width/2))) or (pos[1]-2 == 3 and pos[0] == int((self._width/2))))):
                self._hut2.update_health(damage)
            else:
                self._kingattack = 1

            if((self._kingattack == 1) and (((pos[0]+1 == 28) and pos[1] == 20) or (pos[0]-2 == 28 and pos[1] == 20) or (pos[1]+2 == 20 and pos[0] == 28) or (pos[1]-2 == 20 and pos[0] == 28))):
                self._hut3.update_health(damage)
            else:
                self._kingattack = 1

            if((self._kingattack == 1) and (((pos[0]+1 == int((self._width-15))) and pos[1] == 3) or (pos[0]-2 == int((self._width-15)) and pos[1] == 3) or (pos[1]+2 == 3 and pos[0] == int((self._width-15))) or (pos[1]-2 == 3 and pos[0] == int((self._width-15))))):
                self._hut4.update_health(damage)
            else:
                self._kingattack = 1

            if((self._kingattack == 1) and (((pos[0]+1 == int((self._width-15))) and pos[1] == 20) or (pos[0]-2 == int((self._width-15)) and pos[1] == 20) or (pos[1]+2 == 20 and pos[0] == int((self._width-15))) or (pos[1]-2 == 20 and pos[0] == int((self._width-15))))):
                self._hut5.update_health(damage)
            else:
                self._kingattack = 1

            # cannons

            if((self._kingattack == 0) and (((pos[0]+1 == 56) and pos[1] == 7) or (pos[0]-2 == 56 and pos[1] == 7) or (pos[1]+2 == 7 and pos[0] == 56) or (pos[1]-2 == 7 and pos[0] == 56))):
                self._cannon1.update_health(damage)
            else:
                self._kingattack = 1
            if((self._kingattack == 0) and (((pos[0]+1 == 120) and pos[1] == 23) or (pos[0]-2 == 120 and pos[1] == 23) or (pos[1]+2 == 23 and pos[0] == 120) or (pos[1]-2 == 23 and pos[0] == 120))):
                self._cannon2.update_health(damage)
            else:
                self._kingattack = 1

            # Walls
            if((pos[0]+1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) - 5+1)) or (pos[0]-1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) - 5+1))):
                self._wall_left1.update_health(damage)
            if((pos[0]+1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) - 3)) or (pos[0]-1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) - 3))):
                self._wall_left2.update_health(damage)
            if((pos[0]+1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) - 2)) or (pos[0]-1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) - 2))):
                self._wall_left3.update_health(damage)
            if((pos[0]+1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) - 1)) or (pos[0]-1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) - 1))):
                self._wall_left4.update_health(damage)
            if((pos[0]+1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2))) or (pos[0]-1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2)))):
                self._wall_left5.update_health(damage)
            if((pos[0]+1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) + 1)) or (pos[0]-1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) + 1))):
                self._wall_left6.update_health(damage)
            if((pos[0]+1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) + 2)) or (pos[0]-1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) + 2))):
                self._wall_left7.update_health(damage)
            if((pos[0]+1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) + 3)) or (pos[0]-1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) + 3))):
                self._wall_left8.update_health(damage)
            if((pos[0]+1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) + 4)) or (pos[0]-1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) + 4))):
                self._wall_left9.update_health(damage)

            # right
            if((pos[0]+1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) - 5+1)) or (pos[0]-1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) - 5+1))):
                self._wall_right1.update_health(damage)
            if((pos[0]+1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) - 3)) or (pos[0]-1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) - 3))):
                self._wall_right2.update_health(damage)
            if((pos[0]+1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) - 2)) or (pos[0]-1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) - 2))):
                self._wall_right3.update_health(damage)
            if((pos[0]+1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) - 1)) or (pos[0]-1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) - 1))):
                self._wall_right4.update_health(damage)
            if((pos[0]+1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2))) or (pos[0]-1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2)))):
                self._wall_right5.update_health(damage)
            if((pos[0]+1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) + 1)) or (pos[0]-1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) + 1))):
                self._wall_right6.update_health(damage)
            if((pos[0]+1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) + 2)) or (pos[0]-1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) + 2))):
                self._wall_right7.update_health(damage)
            if((pos[0]+1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) + 3)) or (pos[0]-1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) + 3))):
                self._wall_right8.update_health(damage)
            if((pos[0]+1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) + 4)) or (pos[0]-1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) + 4))):
                self._wall_right9.update_health(damage)

            # up

            if(pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6))):
                if((pos[1]+1 == (int(self._height/2) - 5)) or (pos[1]-1 == (int(self._height/2) - 5))):
                    self._wall_up.update_health(damage)
            # down
            if(pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6))):
                if((pos[1]+1 == (int(self._height/2) - 5+10)) or (pos[1]-1 == (int(self._height/2) - 5+10))):
                    self._wall_down.update_health(damage)
                    
    def queen_attack(self):
        pos, size, height, width, maxsize, health_val, damage = self._queen.get_dimension()

        # print(self._kingattack_falg, "king attack val:",self._kingattack)
        # print(pos[0],pos[1],"width/2:",int(self._width/2),"height/2:",int(self._height/2),"kingattack:",self._kingattack)
        # print("waal1 :",self._wall_left1)
        if(health_val >0):
            
            if(self._queenattack ==0) and (((pos[0]+8 >= int(35) and pos[0] <= int(35))) or ((pos[0]+8 >= int(37) and pos[0] <= int(37))) or ((pos[0]+8 >= int(37) and pos[0] <= int(37)))) and (pos[1] == 12 or pos[1]==14 ):
                self._qhut1.update_health(damage)
                self._qhut2.update_health(damage)
                self._qhut3.update_health(damage)
            if(self._queenattack==0) and ((pos[0]+8 >= int(130) and pos[0] <= int(130))and pos[1]==7):
                self._wizard1.update_health(damage)
            if(self._queenattack==0) and ((pos[1] - 8 <= int(7) and pos[1] >= int(7))and pos[0]==130):
                self._wizard1.update_health(damage)   
            
            if(self._queenattack==0) and ((pos[0]+8 >= int(40) and pos[0] <= int(40))and pos[1]==23):
                self._wizard2.update_health(damage)
            if(self._queenattack==0) and ((pos[1] + 8 >= int(23) and pos[1] <= int(23))and pos[0]==40):
                self._wizard2.update_health(damage) 
                    
            if((self._queenattack == 0) and (pos[0]+8 >= int(self._width/2) and pos[0] <= int(self._width/2)) and ((pos[1] == int(self._height/2 - 2)) or (pos[1] == int(self._height/2 - 1)) or (pos[1] == int(self._height/2)) or (pos[1] == int(self._height/2 + 1)))):
                self._town.update_health(damage)
            else:
                self._queenattack = 1
            if((self._queenattack == 0) and (pos[0]-1-3 == int(self._width/2)) and ((pos[1] == int(self._height/2 - 2)) or (pos[1] == int(self._height/2 - 1)) or (pos[1] == int(self._height/2)) or (pos[1] == int(self._height/2 + 1)))):
                self._town.update_health(damage)
            else:
                self._queenattack = 1

            if((self._queenattack == 0) and (pos[1]+3+8 >= int(self._height/2 - 2)) and ((pos[0] == int(self._width/2)) or (pos[0] == int(self._width/2)) or (pos[0]+1 == int(self._width/2)) or (pos[0]+2 == int(self._width/2)) or (pos[0]+3 == int(self._width/2)))):
                self._town.update_health(damage)
            else:
                self._queenattack = 1
            if((self._queenattack == 0) and (pos[1]-4 == int(self._height/2 - 2)) and ((pos[0] == int(self._width/2)) or (pos[0]+3 == int(self._width/2)) or (pos[0]+4 == int(self._width/2)) or (pos[0]+2 == int(self._width/2)) or (pos[0]+1 == int(self._width/2)))):
                self._town.update_health(damage)
            else:
                self._queenattack = 1

                # huts
            if((self._queenattack == 1) and (((pos[0]+1 == 12) and pos[1] == 3) or (pos[0]-2 == 12 and pos[1] == 3) or (pos[1]+2 == 3 and pos[0] == 12) or (pos[1]-2 == 3 and pos[0] == 12))):
                self._hut1.update_health(damage)
            else:
                self._queenattack = 1
            if((self._queenattack == 1) and (((pos[0]+1 == int((self._width/2))) and pos[1] == 3) or (pos[0]-2 == int((self._width/2)) and pos[1] == 3) or (pos[1]+2 == 3 and pos[0] == int((self._width/2))) or (pos[1]-2 == 3 and pos[0] == int((self._width/2))))):
                self._hut2.update_health(damage)
            else:
                self._queenattack = 1

            if((self._queenattack == 1) and (((pos[0]+1 == 28) and pos[1] == 20) or (pos[0]-2 == 28 and pos[1] == 20) or (pos[1]+2 == 20 and pos[0] == 28) or (pos[1]-2 == 20 and pos[0] == 28))):
                self._hut3.update_health(damage)
            else:
                self._queenattack = 1

            if((self._queenattack == 1) and (((pos[0]+1 == int((self._width-15))) and pos[1] == 3) or (pos[0]-2 == int((self._width-15)) and pos[1] == 3) or (pos[1]+2 == 3 and pos[0] == int((self._width-15))) or (pos[1]-2 == 3 and pos[0] == int((self._width-15))))):
                self._hut4.update_health(damage)
            else:
                self._queenattack = 1

            if((self._queenattack == 1) and (((pos[0]+1 == int((self._width-15))) and pos[1] == 20) or (pos[0]-2 == int((self._width-15)) and pos[1] == 20) or (pos[1]+2 == 20 and pos[0] == int((self._width-15))) or (pos[1]-2 == 20 and pos[0] == int((self._width-15))))):
                self._hut5.update_health(damage)
            else:
                self._queenattack = 1

            # cannons

            if((self._queenattack == 0) and (((pos[0]+1 == 56) and pos[1] == 7) or (pos[0]-2 == 56 and pos[1] == 7) or (pos[1]+2 == 7 and pos[0] == 56) or (pos[1]-2 == 7 and pos[0] == 56))):
                self._cannon1.update_health(damage)
            else:
                self._queenattack = 1
            if((self._queenattack == 0) and (((pos[0]+1 == 120) and pos[1] == 23) or (pos[0]-2 == 120 and pos[1] == 23) or (pos[1]+2 == 23 and pos[0] == 120) or (pos[1]-2 == 23 and pos[0] == 120))):
                self._cannon2.update_health(damage)
            else:
                self._queenattack = 1

            # Walls
            if((pos[0]+1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) - 5+1)) or (pos[0]-1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) - 5+1))):
                self._wall_left1.update_health(damage)
            if((pos[0]+1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) - 3)) or (pos[0]-1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) - 3))):
                self._wall_left2.update_health(damage)
            if((pos[0]+1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) - 2)) or (pos[0]-1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) - 2))):
                self._wall_left3.update_health(damage)
            if((pos[0]+1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) - 1)) or (pos[0]-1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) - 1))):
                self._wall_left4.update_health(damage)
            if((pos[0]+1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2))) or (pos[0]-1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2)))):
                self._wall_left5.update_health(damage)
            if((pos[0]+1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) + 1)) or (pos[0]-1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) + 1))):
                self._wall_left6.update_health(damage)
            if((pos[0]+1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) + 2)) or (pos[0]-1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) + 2))):
                self._wall_left7.update_health(damage)
            if((pos[0]+1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) + 3)) or (pos[0]-1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) + 3))):
                self._wall_left8.update_health(damage)
            if((pos[0]+1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) + 4)) or (pos[0]-1 == int(self._width/2)-6) and (pos[1] == (int(self._height/2) + 4))):
                self._wall_left9.update_health(damage)

            # right
            if((pos[0]+1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) - 5+1)) or (pos[0]-1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) - 5+1))):
                self._wall_right1.update_health(damage)
            if((pos[0]+1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) - 3)) or (pos[0]-1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) - 3))):
                self._wall_right2.update_health(damage)
            if((pos[0]+1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) - 2)) or (pos[0]-1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) - 2))):
                self._wall_right3.update_health(damage)
            if((pos[0]+1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) - 1)) or (pos[0]-1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) - 1))):
                self._wall_right4.update_health(damage)
            if((pos[0]+1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2))) or (pos[0]-1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2)))):
                self._wall_right5.update_health(damage)
            if((pos[0]+1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) + 1)) or (pos[0]-1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) + 1))):
                self._wall_right6.update_health(damage)
            if((pos[0]+1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) + 2)) or (pos[0]-1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) + 2))):
                self._wall_right7.update_health(damage)
            if((pos[0]+1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) + 3)) or (pos[0]-1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) + 3))):
                self._wall_right8.update_health(damage)
            if((pos[0]+1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) + 4)) or (pos[0]-1 == int(self._width/2)+12) and (pos[1] == (int(self._height/2) + 4))):
                self._wall_right9.update_health(damage)

            # up

            if(pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6))):
                if((pos[1]+1 == (int(self._height/2) - 5)) or (pos[1]-1 == (int(self._height/2) - 5))):
                    self._wall_up.update_health(damage)
            # down
            if(pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6))):
                if((pos[1]+1 == (int(self._height/2) - 5+10)) or (pos[1]-1 == (int(self._height/2) - 5+10))):
                    self._wall_down.update_health(damage)


    # def king_val(self):
    #     self._queenattack = 1

    def result(self):
        
        if(self._town._health_val<=0 and self._hut1._health_val<=0 and self._hut2._health_val<=0 and self._hut3._health_val<=0 and self._hut4._health_val<=0 and self._hut5._health_val<=0):
            self._screen.game_won()
            
        elif(self._king._health_val<=0 
            #  and self._barbarian_k._health_val<=0 and self._barbarian_k1._health_val<=0 and self._barbarian_k2._health_val<=0 and self._barbarian_l1._health_val<=0 and self._barbarian_l2._health_val<=0 and self._barbarian_l._health_val<=0 and self._barbarian_p._health_val<=0  and self._barbarian_p1._health_val<=0  and self._barbarian_p2._health_val<=0  ):
        ):
            self._screen.game_lost()
            
# v counter
# c counter
# x counter
    def Balloon_attackx1(self):
        h1 = self._hut1.hut_health()
        h2 = self._hut2.hut_health()
        h3 = self._hut3.hut_health()
        h4 = self._hut4.hut_health()
        h5 = self._hut5.hut_health()
        c1 = self._cannon1.can_health()
        c2 = self._cannon2.can_health()
        w1 = self._wizard1.can_health()
        w2 = self._wizard2.can_health()
        town = self._town.get_health()
        print(w1,w2,c1,c2," balloon",end=" ")
        self._pri = [w1,w2,c1,c2]
        self._listh = [h1, h2, h3, h4, h5, town]
        pos, size, height, width, maxsize, health_val, damage = self._xBalloon2.get_dimension()
        can1 = self._cannon1.can_health()
        can2 = self._cannon2.can_health()
        if(health_val > 0):
            mx = 100000
            index = 10
            for i in range(4):
                if(self._pri[i]>0):
                    dif = abs(self._prix[i]-pos[0])+abs(self._priy[i]-pos[1])
                
                    if(dif < mx):
                        mx = dif
                        index = i
                        
            print(mx,index,end=" ")            
            
            if(index != 10 and self._prix[index] > pos[0] and self._prix[index] != pos[0]):
                        pos[0] += 1
            elif (index != 10 and self._prix[index] < pos[0] and self._prix[index] != pos[0]):
                        pos[0] -= 1
            elif(index != 10 and self._priy[index] > pos[1] and self._priy[index]-5 != pos[1] and self._prix[index] == pos[0]):
                        pos[1] += 1
            elif (index != 10 and self._priy[index] < pos[1] and self._priy[index]+5 != pos[1] and self._prix[index] == pos[0]):
                        pos[1] -= 1
            else:
                if(index == 0):
                    self._wizard1.update_health(damage)

                    if(self._wizard1.can_health() == 0):

                        mm = 10000

                if(index == 1):

                    self._wizard2.update_health(damage)
                    if(self._wizard2.can_health() == 0):
                                mm = 10000
                if(index == 2):

                    self._cannon1.update_health(damage)
                    if(self._cannon1.can_health() == 0):
                                mm = 10000
                if(index == 3):

                    self._cannon2.update_health(damage)
                    if(self._cannon2.can_health() == 0):
                                mm = 10000

            if(w1 <=0 and w2 <=0 and c1<=0 and c2 <=0):
                mm = 10000
                index = 10
                for i in range(5):

                    if(self._listh[i] > 0):

                        dif = abs(self._listx[i]-pos[0])+abs(self._listy[i]-pos[1])
                        if(dif < mm):
                            mm = dif
                            index = i

                if((can1 > 0) and (((pos[0]+2 == 56) and pos[1] == 7) or (pos[0]-2 == 56 and pos[1] == 7) or (pos[1]+2 == 7 and pos[0] == 56) or (pos[1]-2 == 7 and pos[0] == 56))):
                    self._cannon1.update_health(damage)

                elif((can2 > 0) and (((pos[0]+2 == 120) and pos[1] == 23) or (pos[0]-2 == 120 and pos[1] == 23) or (pos[1]+2 == 23 and pos[0] == 120) or (pos[1]-2 == 23 and pos[0] == 120))):
                    self._cannon2.update_health(damage)
                else:

                    # print("destyination:",self._listx[index],self._listy[ index],"index",index,end=" ")
                    if(index != 10 and self._listx[index] > pos[0] and self._listx[index] != pos[0]):
                        pos[0] += 1
                    elif (index != 10 and self._listx[index] < pos[0] and self._listx[index] != pos[0]):
                        pos[0] -= 1
                    elif(index != 10 and self._listy[index] > pos[1] and self._listy[index]-5 != pos[1] and self._listx[index] == pos[0]):
                        pos[1] += 1
                    elif (index != 10 and self._listy[index] < pos[1] and self._listy[index]+5 != pos[1] and self._listx[index] == pos[0]):
                        pos[1] -= 1
                    else:
                        if(index == 0):
                            self._hut1.update_health(damage)

                            if(self._hut1.hut_health() == 0):

                                mm = 10000

                        if(index == 1):

                            self._hut2.update_health(damage)
                            if(self._hut2.hut_health() == 0):
                                mm = 10000
                        if(index == 2):

                            self._hut3.update_health(damage)
                            if(self._hut3.hut_health() == 0):
                                mm = 10000
                        if(index == 3):

                            self._hut4.update_health(damage)
                            if(self._hut4.hut_health() == 0):
                                mm = 10000
                        if(index == 4):

                            self._hut5.update_health(damage)
                            if(self._hut5.hut_health() == 0):
                                mm = 10000
    def Balloon_attackx(self):
        h1 = self._hut1.hut_health()
        h2 = self._hut2.hut_health()
        h3 = self._hut3.hut_health()
        h4 = self._hut4.hut_health()
        h5 = self._hut5.hut_health()
        c1 = self._cannon1.can_health()
        c2 = self._cannon2.can_health()
        w1 = self._wizard1.can_health()
        w2 = self._wizard2.can_health()
        town = self._town.get_health()
        print(w1,w2,c1,c2," balloon",end=" ")
        self._pri = [w1,w2,c1,c2]
        self._listh = [h1, h2, h3, h4, h5, town]
        pos, size, height, width, maxsize, health_val, damage = self._xBalloon1.get_dimension()
        can1 = self._cannon1.can_health()
        can2 = self._cannon2.can_health()
        
        if(health_val > 0):
            mx = 100000
            index = 10
            for i in range(4):
                if(self._pri[i]>0):
                    dif = abs(self._prix[i]-pos[0])+abs(self._priy[i]-pos[1])
                
                    if(dif < mx):
                        mx = dif
                        index = i
                        
            print(mx,index,end=" ")            
            
            if(index != 10 and self._prix[index] > pos[0] and self._prix[index] != pos[0]):
                        pos[0] += 1
            elif (index != 10 and self._prix[index] < pos[0] and self._prix[index] != pos[0]):
                        pos[0] -= 1
            elif(index != 10 and self._priy[index] > pos[1] and self._priy[index]-5 != pos[1] and self._prix[index] == pos[0]):
                        pos[1] += 1
            elif (index != 10 and self._priy[index] < pos[1] and self._priy[index]+5 != pos[1] and self._prix[index] == pos[0]):
                        pos[1] -= 1
            else:
                if(index == 0):
                    self._wizard1.update_health(damage)

                    if(self._wizard1.can_health() == 0):

                        mm = 10000

                if(index == 1):

                    self._wizard2.update_health(damage)
                    if(self._wizard2.can_health() == 0):
                                mm = 10000
                if(index == 2):

                    self._cannon1.update_health(damage)
                    if(self._cannon1.can_health() == 0):
                                mm = 10000
                if(index == 3):

                    self._cannon2.update_health(damage)
                    if(self._cannon2.can_health() == 0):
                                mm = 10000

            if(w1 <=0 and w2 <=0 and c1<=0 and c2 <=0):
                mm = 10000
                index = 10
                for i in range(5):

                    if(self._listh[i] > 0):

                        dif = abs(self._listx[i]-pos[0])+abs(self._listy[i]-pos[1])
                        if(dif < mm):
                            mm = dif
                            index = i

                if((can1 > 0) and (((pos[0]+2 == 56) and pos[1] == 7) or (pos[0]-2 == 56 and pos[1] == 7) or (pos[1]+2 == 7 and pos[0] == 56) or (pos[1]-2 == 7 and pos[0] == 56))):
                    self._cannon1.update_health(damage)

                elif((can2 > 0) and (((pos[0]+2 == 120) and pos[1] == 23) or (pos[0]-2 == 120 and pos[1] == 23) or (pos[1]+2 == 23 and pos[0] == 120) or (pos[1]-2 == 23 and pos[0] == 120))):
                    self._cannon2.update_health(damage)
                else:

                    # print("destyination:",self._listx[index],self._listy[ index],"index",index,end=" ")
                    if(index != 10 and self._listx[index] > pos[0] and self._listx[index] != pos[0]):
                        pos[0] += 1
                    elif (index != 10 and self._listx[index] < pos[0] and self._listx[index] != pos[0]):
                        pos[0] -= 1
                    elif(index != 10 and self._listy[index] > pos[1] and self._listy[index]-5 != pos[1] and self._listx[index] == pos[0]):
                        pos[1] += 1
                    elif (index != 10 and self._listy[index] < pos[1] and self._listy[index]+5 != pos[1] and self._listx[index] == pos[0]):
                        pos[1] -= 1
                    else:
                        if(index == 0):
                            self._hut1.update_health(damage)

                            if(self._hut1.hut_health() == 0):

                                mm = 10000

                        if(index == 1):

                            self._hut2.update_health(damage)
                            if(self._hut2.hut_health() == 0):
                                mm = 10000
                        if(index == 2):

                            self._hut3.update_health(damage)
                            if(self._hut3.hut_health() == 0):
                                mm = 10000
                        if(index == 3):

                            self._hut4.update_health(damage)
                            if(self._hut4.hut_health() == 0):
                                mm = 10000
                        if(index == 4):

                            self._hut5.update_health(damage)
                            if(self._hut5.hut_health() == 0):
                                mm = 10000
    def Balloon_attackc1(self):
        h1 = self._hut1.hut_health()
        h2 = self._hut2.hut_health()
        h3 = self._hut3.hut_health()
        h4 = self._hut4.hut_health()
        h5 = self._hut5.hut_health()
        c1 = self._cannon1.can_health()
        c2 = self._cannon2.can_health()
        w1 = self._wizard1.can_health()
        w2 = self._wizard2.can_health()
        town = self._town.get_health()
        print(w1,w2,c1,c2," balloon",end=" ")
        self._pri = [w1,w2,c1,c2]
        self._listh = [h1, h2, h3, h4, h5, town]
        pos, size, height, width, maxsize, health_val, damage = self._cBalloon2.get_dimension()
        can1 = self._cannon1.can_health()
        can2 = self._cannon2.can_health()
        if(health_val > 0):
            mx = 100000
            index = 10
            for i in range(4):
                if(self._pri[i]>0):
                    dif = abs(self._prix[i]-pos[0])+abs(self._priy[i]-pos[1])
                
                    if(dif < mx):
                        mx = dif
                        index = i
                        
            print(mx,index,end=" ")            
            
            if(index != 10 and self._prix[index] > pos[0] and self._prix[index] != pos[0]):
                        pos[0] += 1
            elif (index != 10 and self._prix[index] < pos[0] and self._prix[index] != pos[0]):
                        pos[0] -= 1
            elif(index != 10 and self._priy[index] > pos[1] and self._priy[index]-5 != pos[1] and self._prix[index] == pos[0]):
                        pos[1] += 1
            elif (index != 10 and self._priy[index] < pos[1] and self._priy[index]+5 != pos[1] and self._prix[index] == pos[0]):
                        pos[1] -= 1
            else:
                if(index == 0):
                    self._wizard1.update_health(damage)

                    if(self._wizard1.can_health() == 0):

                        mm = 10000

                if(index == 1):

                    self._wizard2.update_health(damage)
                    if(self._wizard2.can_health() == 0):
                                mm = 10000
                if(index == 2):

                    self._cannon1.update_health(damage)
                    if(self._cannon1.can_health() == 0):
                                mm = 10000
                if(index == 3):

                    self._cannon2.update_health(damage)
                    if(self._cannon2.can_health() == 0):
                                mm = 10000

            if(w1 <=0 and w2 <=0 and c1<=0 and c2 <=0):
                mm = 10000
                index = 10
                for i in range(5):

                    if(self._listh[i] > 0):

                        dif = abs(self._listx[i]-pos[0])+abs(self._listy[i]-pos[1])
                        if(dif < mm):
                            mm = dif
                            index = i

                if((can1 > 0) and (((pos[0]+2 == 56) and pos[1] == 7) or (pos[0]-2 == 56 and pos[1] == 7) or (pos[1]+2 == 7 and pos[0] == 56) or (pos[1]-2 == 7 and pos[0] == 56))):
                    self._cannon1.update_health(damage)

                elif((can2 > 0) and (((pos[0]+2 == 120) and pos[1] == 23) or (pos[0]-2 == 120 and pos[1] == 23) or (pos[1]+2 == 23 and pos[0] == 120) or (pos[1]-2 == 23 and pos[0] == 120))):
                    self._cannon2.update_health(damage)
                else:

                    # print("destyination:",self._listx[index],self._listy[ index],"index",index,end=" ")
                    if(index != 10 and self._listx[index] > pos[0] and self._listx[index] != pos[0]):
                        pos[0] += 1
                    elif (index != 10 and self._listx[index] < pos[0] and self._listx[index] != pos[0]):
                        pos[0] -= 1
                    elif(index != 10 and self._listy[index] > pos[1] and self._listy[index]-5 != pos[1] and self._listx[index] == pos[0]):
                        pos[1] += 1
                    elif (index != 10 and self._listy[index] < pos[1] and self._listy[index]+5 != pos[1] and self._listx[index] == pos[0]):
                        pos[1] -= 1
                    else:
                        if(index == 0):
                            self._hut1.update_health(damage)

                            if(self._hut1.hut_health() == 0):

                                mm = 10000

                        if(index == 1):

                            self._hut2.update_health(damage)
                            if(self._hut2.hut_health() == 0):
                                mm = 10000
                        if(index == 2):

                            self._hut3.update_health(damage)
                            if(self._hut3.hut_health() == 0):
                                mm = 10000
                        if(index == 3):

                            self._hut4.update_health(damage)
                            if(self._hut4.hut_health() == 0):
                                mm = 10000
                        if(index == 4):

                            self._hut5.update_health(damage)
                            if(self._hut5.hut_health() == 0):
                                mm = 10000
    def Balloon_attackc(self):
        h1 = self._hut1.hut_health()
        h2 = self._hut2.hut_health()
        h3 = self._hut3.hut_health()
        h4 = self._hut4.hut_health()
        h5 = self._hut5.hut_health()
        c1 = self._cannon1.can_health()
        c2 = self._cannon2.can_health()
        w1 = self._wizard1.can_health()
        w2 = self._wizard2.can_health()
        town = self._town.get_health()
        self._pri = [w1,w2,c1,c2]
        self._listh = [h1, h2, h3, h4, h5, town]
        pos, size, height, width, maxsize, health_val, damage = self._cBalloon1.get_dimension()
        can1 = self._cannon1.can_health()
        can2 = self._cannon2.can_health()
        if(health_val > 0):
            mx = 100000
            index = 10
            for i in range(4):
                if(self._pri[i]>0):
                    dif = abs(self._prix[i]-pos[0])+abs(self._priy[i]-pos[1])
                
                    if(dif < mx):
                        mx = dif
                        index = i
                        
            print(mx,index,end=" ")            
            
            if(index != 10 and self._prix[index] > pos[0] and self._prix[index] != pos[0]):
                        pos[0] += 1
            elif (index != 10 and self._prix[index] < pos[0] and self._prix[index] != pos[0]):
                        pos[0] -= 1
            elif(index != 10 and self._priy[index] > pos[1] and self._priy[index]-5 != pos[1] and self._prix[index] == pos[0]):
                        pos[1] += 1
            elif (index != 10 and self._priy[index] < pos[1] and self._priy[index]+5 != pos[1] and self._prix[index] == pos[0]):
                        pos[1] -= 1
            else:
                if(index == 0):
                    self._wizard1.update_health(damage)

                    if(self._wizard1.can_health() == 0):

                        mm = 10000

                if(index == 1):

                    self._wizard2.update_health(damage)
                    if(self._wizard2.can_health() == 0):
                                mm = 10000
                if(index == 2):

                    self._cannon1.update_health(damage)
                    if(self._cannon1.can_health() == 0):
                                mm = 10000
                if(index == 3):

                    self._cannon2.update_health(damage)
                    if(self._cannon2.can_health() == 0):
                                mm = 10000

            if(w1 <=0 and w2 <=0 and c1<=0 and c2 <=0):
                mm = 10000
                index = 10
                for i in range(5):

                    if(self._listh[i] > 0):

                        dif = abs(self._listx[i]-pos[0])+abs(self._listy[i]-pos[1])
                        if(dif < mm):
                            mm = dif
                            index = i

                if((can1 > 0) and (((pos[0]+2 == 56) and pos[1] == 7) or (pos[0]-2 == 56 and pos[1] == 7) or (pos[1]+2 == 7 and pos[0] == 56) or (pos[1]-2 == 7 and pos[0] == 56))):
                    self._cannon1.update_health(damage)

                elif((can2 > 0) and (((pos[0]+2 == 120) and pos[1] == 23) or (pos[0]-2 == 120 and pos[1] == 23) or (pos[1]+2 == 23 and pos[0] == 120) or (pos[1]-2 == 23 and pos[0] == 120))):
                    self._cannon2.update_health(damage)
                else:

                    # print("destyination:",self._listx[index],self._listy[ index],"index",index,end=" ")
                    if(index != 10 and self._listx[index] > pos[0] and self._listx[index] != pos[0]):
                        pos[0] += 1
                    elif (index != 10 and self._listx[index] < pos[0] and self._listx[index] != pos[0]):
                        pos[0] -= 1
                    elif(index != 10 and self._listy[index] > pos[1] and self._listy[index]-5 != pos[1] and self._listx[index] == pos[0]):
                        pos[1] += 1
                    elif (index != 10 and self._listy[index] < pos[1] and self._listy[index]+5 != pos[1] and self._listx[index] == pos[0]):
                        pos[1] -= 1
                    else:
                        if(index == 0):
                            self._hut1.update_health(damage)

                            if(self._hut1.hut_health() == 0):

                                mm = 10000

                        if(index == 1):

                            self._hut2.update_health(damage)
                            if(self._hut2.hut_health() == 0):
                                mm = 10000
                        if(index == 2):

                            self._hut3.update_health(damage)
                            if(self._hut3.hut_health() == 0):
                                mm = 10000
                        if(index == 3):

                            self._hut4.update_health(damage)
                            if(self._hut4.hut_health() == 0):
                                mm = 10000
                        if(index == 4):

                            self._hut5.update_health(damage)
                            if(self._hut5.hut_health() == 0):
                                mm = 10000
        
    def Balloon_attack1(self):
        h1 = self._hut1.hut_health()
        h2 = self._hut2.hut_health()
        h3 = self._hut3.hut_health()
        h4 = self._hut4.hut_health()
        h5 = self._hut5.hut_health()
        c1 = self._cannon1.can_health()
        c2 = self._cannon2.can_health()
        w1 = self._wizard1.can_health()
        w2 = self._wizard2.can_health()
        town = self._town.get_health()
        print(w1,w2,c1,c2," balloon",end=" ")
        self._pri = [w1,w2,c1,c2]
        self._listh = [h1, h2, h3, h4, h5, town]
        pos, size, height, width, maxsize, health_val, damage = self._Balloon2.get_dimension()
        can1 = self._cannon1.can_health()
        can2 = self._cannon2.can_health()
        if(health_val > 0):
            mx = 100000
            index = 10
            for i in range(4):
                if(self._pri[i]>0):
                    dif = abs(self._prix[i]-pos[0])+abs(self._priy[i]-pos[1])
                
                    if(dif < mx):
                        mx = dif
                        index = i
                        
            print(mx,index,end=" ")            
            
            if(index != 10 and self._prix[index] > pos[0] and self._prix[index] != pos[0]):
                        pos[0] += 1
            elif (index != 10 and self._prix[index] < pos[0] and self._prix[index] != pos[0]):
                        pos[0] -= 1
            elif(index != 10 and self._priy[index] > pos[1] and self._priy[index]-5 != pos[1] and self._prix[index] == pos[0]):
                        pos[1] += 1
            elif (index != 10 and self._priy[index] < pos[1] and self._priy[index]+5 != pos[1] and self._prix[index] == pos[0]):
                        pos[1] -= 1
            else:
                if(index == 0):
                    self._wizard1.update_health(damage)

                    if(self._wizard1.can_health() == 0):

                        mm = 10000

                if(index == 1):

                    self._wizard2.update_health(damage)
                    if(self._wizard2.can_health() == 0):
                                mm = 10000
                if(index == 2):

                    self._cannon1.update_health(damage)
                    if(self._cannon1.can_health() == 0):
                                mm = 10000
                if(index == 3):

                    self._cannon2.update_health(damage)
                    if(self._cannon2.can_health() == 0):
                                mm = 10000

            if(w1 <=0 and w2 <=0 and c1<=0 and c2 <=0):
                mm = 10000
                index = 10
                for i in range(5):

                    if(self._listh[i] > 0):

                        dif = abs(self._listx[i]-pos[0])+abs(self._listy[i]-pos[1])
                        if(dif < mm):
                            mm = dif
                            index = i

                if((can1 > 0) and (((pos[0]+2 == 56) and pos[1] == 7) or (pos[0]-2 == 56 and pos[1] == 7) or (pos[1]+2 == 7 and pos[0] == 56) or (pos[1]-2 == 7 and pos[0] == 56))):
                    self._cannon1.update_health(damage)

                elif((can2 > 0) and (((pos[0]+2 == 120) and pos[1] == 23) or (pos[0]-2 == 120 and pos[1] == 23) or (pos[1]+2 == 23 and pos[0] == 120) or (pos[1]-2 == 23 and pos[0] == 120))):
                    self._cannon2.update_health(damage)
                else:

                    # print("destyination:",self._listx[index],self._listy[ index],"index",index,end=" ")
                    if(index != 10 and self._listx[index] > pos[0] and self._listx[index] != pos[0]):
                        pos[0] += 1
                    elif (index != 10 and self._listx[index] < pos[0] and self._listx[index] != pos[0]):
                        pos[0] -= 1
                    elif(index != 10 and self._listy[index] > pos[1] and self._listy[index]-5 != pos[1] and self._listx[index] == pos[0]):
                        pos[1] += 1
                    elif (index != 10 and self._listy[index] < pos[1] and self._listy[index]+5 != pos[1] and self._listx[index] == pos[0]):
                        pos[1] -= 1
                    else:
                        if(index == 0):
                            self._hut1.update_health(damage)

                            if(self._hut1.hut_health() == 0):

                                mm = 10000

                        if(index == 1):

                            self._hut2.update_health(damage)
                            if(self._hut2.hut_health() == 0):
                                mm = 10000
                        if(index == 2):

                            self._hut3.update_health(damage)
                            if(self._hut3.hut_health() == 0):
                                mm = 10000
                        if(index == 3):

                            self._hut4.update_health(damage)
                            if(self._hut4.hut_health() == 0):
                                mm = 10000
                        if(index == 4):

                            self._hut5.update_health(damage)
                            if(self._hut5.hut_health() == 0):
                                mm = 10000
                            
    def Balloon_attack(self):
        h1 = self._hut1.hut_health()
        h2 = self._hut2.hut_health()
        h3 = self._hut3.hut_health()
        h4 = self._hut4.hut_health()
        h5 = self._hut5.hut_health()
        c1 = self._cannon1.can_health()
        c2 = self._cannon2.can_health()
        w1 = self._wizard1.can_health()
        w2 = self._wizard2.can_health()
        town = self._town.get_health()
        print(w1,w2,c1,c2," balloon",end=" ")
        self._pri = [w1,w2,c1,c2]
        self._listh = [h1, h2, h3, h4, h5, town]
        pos, size, height, width, maxsize, health_val, damage = self._Balloon1.get_dimension()
        can1 = self._cannon1.can_health()
        can2 = self._cannon2.can_health()
        if(health_val > 0):
            mx = 100000
            index = 10
            for i in range(4):
                if(self._pri[i]>0):
                    dif = abs(self._prix[i]-pos[0])+abs(self._priy[i]-pos[1])
                
                    if(dif < mx):
                        mx = dif
                        index = i
                        
            print(mx,index,end=" ")            
            
            if(index != 10 and self._prix[index] > pos[0] and self._prix[index] != pos[0]):
                        pos[0] += 1
            elif (index != 10 and self._prix[index] < pos[0] and self._prix[index] != pos[0]):
                        pos[0] -= 1
            elif(index != 10 and self._priy[index] > pos[1] and self._priy[index]-5 != pos[1] and self._prix[index] == pos[0]):
                        pos[1] += 1
            elif (index != 10 and self._priy[index] < pos[1] and self._priy[index]+5 != pos[1] and self._prix[index] == pos[0]):
                        pos[1] -= 1
            else:
                if(index == 0):
                    self._wizard1.update_health(damage)

                    if(self._wizard1.can_health() == 0):

                        mm = 10000

                if(index == 1):

                    self._wizard2.update_health(damage)
                    if(self._wizard2.can_health() == 0):
                                mm = 10000
                if(index == 2):

                    self._cannon1.update_health(damage)
                    if(self._cannon1.can_health() == 0):
                                mm = 10000
                if(index == 3):

                    self._cannon2.update_health(damage)
                    if(self._cannon2.can_health() == 0):
                                mm = 10000

            if(w1 <=0 and w2 <=0 and c1<=0 and c2 <=0):
                mm = 10000
                index = 10
                for i in range(5):

                    if(self._listh[i] > 0):

                        dif = abs(self._listx[i]-pos[0])+abs(self._listy[i]-pos[1])
                        if(dif < mm):
                            mm = dif
                            index = i

                if((can1 > 0) and (((pos[0]+2 == 56) and pos[1] == 7) or (pos[0]-2 == 56 and pos[1] == 7) or (pos[1]+2 == 7 and pos[0] == 56) or (pos[1]-2 == 7 and pos[0] == 56))):
                    self._cannon1.update_health(damage)

                elif((can2 > 0) and (((pos[0]+2 == 120) and pos[1] == 23) or (pos[0]-2 == 120 and pos[1] == 23) or (pos[1]+2 == 23 and pos[0] == 120) or (pos[1]-2 == 23 and pos[0] == 120))):
                    self._cannon2.update_health(damage)
                else:

                    # print("destyination:",self._listx[index],self._listy[ index],"index",index,end=" ")
                    if(index != 10 and self._listx[index] > pos[0] and self._listx[index] != pos[0]):
                        pos[0] += 1
                    elif (index != 10 and self._listx[index] < pos[0] and self._listx[index] != pos[0]):
                        pos[0] -= 1
                    elif(index != 10 and self._listy[index] > pos[1] and self._listy[index]-5 != pos[1] and self._listx[index] == pos[0]):
                        pos[1] += 1
                    elif (index != 10 and self._listy[index] < pos[1] and self._listy[index]+5 != pos[1] and self._listx[index] == pos[0]):
                        pos[1] -= 1
                    else:
                        if(index == 0):
                            self._hut1.update_health(damage)

                            if(self._hut1.hut_health() == 0):

                                mm = 10000

                        if(index == 1):

                            self._hut2.update_health(damage)
                            if(self._hut2.hut_health() == 0):
                                mm = 10000
                        if(index == 2):

                            self._hut3.update_health(damage)
                            if(self._hut3.hut_health() == 0):
                                mm = 10000
                        if(index == 3):

                            self._hut4.update_health(damage)
                            if(self._hut4.hut_health() == 0):
                                mm = 10000
                        if(index == 4):

                            self._hut5.update_health(damage)
                            if(self._hut5.hut_health() == 0):
                                mm = 10000
    
            
# n counter
    def archer_nattackm2(self):
        h1 = self._hut1.hut_health()
        h2 = self._hut2.hut_health()
        h3 = self._hut3.hut_health()
        h4 = self._hut4.hut_health()
        h5 = self._hut5.hut_health()
        c1 = self._cannon1.can_health()
        c2 = self._cannon2.can_health()
        town = self._town.get_health()
        self._listh = [h1, h2, h3, h4, h5, c1, c2, town]
        pos, size, height, width, maxsize, health_val, damage = self._narcher2.get_dimension()
        wall_health = self._wall_down.wall_health()
        wall_health_up = self._wall_up.wall_health()
        can1 = self._cannon1.can_health()
        can2 = self._cannon2.can_health()

        # print("wall health:",wall_hea
        # lth,end=" ")
        mm = 10000
        index = 10
        for i in range(7):

            if(self._listh[i] > 0):

                dif = abs(self._listx[i]-pos[0])+abs(self._listy[i]-pos[1])
                if(dif < mm):
                    mm = dif
                    index = i
        if((wall_health > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6))) and ((pos[1]+1 == (int(self._height/2) - 5+10)) or (pos[1]-1 == (int(self._height/2) - 5+10)))):
            self._wall_down.update_health(damage)
            #
        elif(((wall_health_up > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6)))) and (((pos[1]+1 == (int(self._height/2) - 5)) or (pos[1]-1 == (int(self._height/2) - 5))))):
            self._wall_up.update_health(damage)

        elif((can1 > 0) and (((pos[0]+2 == 56) and pos[1] == 7) or (pos[0]-2 == 56 and pos[1] == 7) or (pos[1]+2 == 7 and pos[0] == 56) or (pos[1]-2 == 7 and pos[0] == 56))):
            self._cannon1.update_health(damage)

        elif((can2 > 0) and (((pos[0]+2 == 120) and pos[1] == 23) or (pos[0]-2 == 120 and pos[1] == 23) or (pos[1]+2 == 23 and pos[0] == 120) or (pos[1]-2 == 23 and pos[0] == 120))):
            self._cannon2.update_health(damage)
        else:

            # print("destyination:",self._listx[index],self._listy[ index],"index",index,end=" ")
            if(index != 10 and self._listx[index] > pos[0] and self._listx[index] != pos[0]):
                pos[0] += 1
            elif (index != 10 and self._listx[index] < pos[0] and self._listx[index] != pos[0]):
                pos[0] -= 1
            elif(index != 10 and self._listy[index] > pos[1] and self._listy[index]-5 != pos[1] and self._listx[index] == pos[0]):
                pos[1] += 1
            elif (index != 10 and self._listy[index] < pos[1] and self._listy[index]+5 != pos[1] and self._listx[index] == pos[0]):
                pos[1] -= 1
            else:
                if(index == 0):
                    self._hut1.update_health(damage)

                    if(self._hut1.hut_health() == 0):

                        mm = 10000

                        # self.barbarian_attack1()
                if(index == 1):

                    self._hut2.update_health(damage)
                    if(self._hut2.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 2):

                    self._hut3.update_health(damage)
                    if(self._hut3.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 3):

                    self._hut4.update_health(damage)
                    if(self._hut4.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 4):

                    self._hut5.update_health(damage)
                    if(self._hut5.hut_health() == 0):
                        mm = 10000
                if(index == 5):
                    self._cannon1.update_health(damage)
                    if(self._cannon1.can_health() == 0):
                        mm = 10000
                if(index == 6):
                    self._cannon2.update_health(damage)
                    if(self._cannon2.can_health() == 0):
                        mm = 10000
                if(index == 7):
                    self._town.update_health(damage)
                    if(self._town.get_health() == 0):
                        mm = 10000
    def archer_nattackm1(self):
        h1 = self._hut1.hut_health()
        h2 = self._hut2.hut_health()
        h3 = self._hut3.hut_health()
        h4 = self._hut4.hut_health()
        h5 = self._hut5.hut_health()
        c1 = self._cannon1.can_health()
        c2 = self._cannon2.can_health()
        town = self._town.get_health()
        self._listh = [h1, h2, h3, h4, h5, c1, c2, town]
        pos, size, height, width, maxsize, health_val, damage = self._narcher1.get_dimension()
        wall_health = self._wall_down.wall_health()
        wall_health_up = self._wall_up.wall_health()
        can1 = self._cannon1.can_health()
        can2 = self._cannon2.can_health()

        # print("wall health:",wall_hea
        # lth,end=" ")
        mm = 10000
        index = 10
        for i in range(7):

            if(self._listh[i] > 0):

                dif = abs(self._listx[i]-pos[0])+abs(self._listy[i]-pos[1])
                if(dif < mm):
                    mm = dif
                    index = i
        if((wall_health > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6))) and ((pos[1]+1 == (int(self._height/2) - 5+10)) or (pos[1]-1 == (int(self._height/2) - 5+10)))):
            self._wall_down.update_health(damage)
            #
        elif(((wall_health_up > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6)))) and (((pos[1]+1 == (int(self._height/2) - 5)) or (pos[1]-1 == (int(self._height/2) - 5))))):
            self._wall_up.update_health(damage)

        elif((can1 > 0) and (((pos[0]+2 == 56) and pos[1] == 7) or (pos[0]-2 == 56 and pos[1] == 7) or (pos[1]+2 == 7 and pos[0] == 56) or (pos[1]-2 == 7 and pos[0] == 56))):
            self._cannon1.update_health(damage)

        elif((can2 > 0) and (((pos[0]+2 == 120) and pos[1] == 23) or (pos[0]-2 == 120 and pos[1] == 23) or (pos[1]+2 == 23 and pos[0] == 120) or (pos[1]-2 == 23 and pos[0] == 120))):
            self._cannon2.update_health(damage)
        else:

            # print("destyination:",self._listx[index],self._listy[ index],"index",index,end=" ")
            if(index != 10 and self._listx[index] > pos[0] and self._listx[index] != pos[0]):
                pos[0] += 1
            elif (index != 10 and self._listx[index] < pos[0] and self._listx[index] != pos[0]):
                pos[0] -= 1
            elif(index != 10 and self._listy[index] > pos[1] and self._listy[index]-5 != pos[1] and self._listx[index] == pos[0]):
                pos[1] += 1
            elif (index != 10 and self._listy[index] < pos[1] and self._listy[index]+5 != pos[1] and self._listx[index] == pos[0]):
                pos[1] -= 1
            else:
                if(index == 0):
                    self._hut1.update_health(damage)

                    if(self._hut1.hut_health() == 0):

                        mm = 10000

                        # self.barbarian_attack1()
                if(index == 1):

                    self._hut2.update_health(damage)
                    if(self._hut2.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 2):

                    self._hut3.update_health(damage)
                    if(self._hut3.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 3):

                    self._hut4.update_health(damage)
                    if(self._hut4.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 4):

                    self._hut5.update_health(damage)
                    if(self._hut5.hut_health() == 0):
                        mm = 10000
                if(index == 5):
                    self._cannon1.update_health(damage)
                    if(self._cannon1.can_health() == 0):
                        mm = 10000
                if(index == 6):
                    self._cannon2.update_health(damage)
                    if(self._cannon2.can_health() == 0):
                        mm = 10000
                if(index == 7):
                    self._town.update_health(damage)
                    if(self._town.get_health() == 0):
                        mm = 10000
                        
# b counter
    def archer_battackm2(self):
        h1 = self._hut1.hut_health()
        h2 = self._hut2.hut_health()
        h3 = self._hut3.hut_health()
        h4 = self._hut4.hut_health()
        h5 = self._hut5.hut_health()
        c1 = self._cannon1.can_health()
        c2 = self._cannon2.can_health()
        town = self._town.get_health()
        self._listh = [h1, h2, h3, h4, h5, c1, c2, town]
        pos, size, height, width, maxsize, health_val, damage = self._barcher2.get_dimension()
        wall_health = self._wall_down.wall_health()
        wall_health_up = self._wall_up.wall_health()
        can1 = self._cannon1.can_health()
        can2 = self._cannon2.can_health()

        # print("wall health:",wall_hea
        # lth,end=" ")
        mm = 10000
        index = 10
        for i in range(7):

            if(self._listh[i] > 0):

                dif = abs(self._listx[i]-pos[0])+abs(self._listy[i]-pos[1])
                if(dif < mm):
                    mm = dif
                    index = i
        if((wall_health > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6))) and ((pos[1]+1 == (int(self._height/2) - 5+10)) or (pos[1]-1 == (int(self._height/2) - 5+10)))):
            self._wall_down.update_health(damage)
            #
        elif(((wall_health_up > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6)))) and (((pos[1]+1 == (int(self._height/2) - 5)) or (pos[1]-1 == (int(self._height/2) - 5))))):
            self._wall_up.update_health(damage)

        elif((can1 > 0) and (((pos[0]+2 == 56) and pos[1] == 7) or (pos[0]-2 == 56 and pos[1] == 7) or (pos[1]+2 == 7 and pos[0] == 56) or (pos[1]-2 == 7 and pos[0] == 56))):
            self._cannon1.update_health(damage)

        elif((can2 > 0) and (((pos[0]+2 == 120) and pos[1] == 23) or (pos[0]-2 == 120 and pos[1] == 23) or (pos[1]+2 == 23 and pos[0] == 120) or (pos[1]-2 == 23 and pos[0] == 120))):
            self._cannon2.update_health(damage)
        else:

            # print("destyination:",self._listx[index],self._listy[ index],"index",index,end=" ")
            if(index != 10 and self._listx[index] > pos[0] and self._listx[index] != pos[0]):
                pos[0] += 1
            elif (index != 10 and self._listx[index] < pos[0] and self._listx[index] != pos[0]):
                pos[0] -= 1
            elif(index != 10 and self._listy[index] > pos[1] and self._listy[index]-5 != pos[1] and self._listx[index] == pos[0]):
                pos[1] += 1
            elif (index != 10 and self._listy[index] < pos[1] and self._listy[index]+5 != pos[1] and self._listx[index] == pos[0]):
                pos[1] -= 1
            else:
                if(index == 0):
                    self._hut1.update_health(damage)

                    if(self._hut1.hut_health() == 0):

                        mm = 10000

                        # self.barbarian_attack1()
                if(index == 1):

                    self._hut2.update_health(damage)
                    if(self._hut2.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 2):

                    self._hut3.update_health(damage)
                    if(self._hut3.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 3):

                    self._hut4.update_health(damage)
                    if(self._hut4.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 4):

                    self._hut5.update_health(damage)
                    if(self._hut5.hut_health() == 0):
                        mm = 10000
                if(index == 5):
                    self._cannon1.update_health(damage)
                    if(self._cannon1.can_health() == 0):
                        mm = 10000
                if(index == 6):
                    self._cannon2.update_health(damage)
                    if(self._cannon2.can_health() == 0):
                        mm = 10000
                if(index == 7):
                    self._town.update_health(damage)
                    if(self._town.get_health() == 0):
                        mm = 10000
    def archer_battackm1(self):
        h1 = self._hut1.hut_health()
        h2 = self._hut2.hut_health()
        h3 = self._hut3.hut_health()
        h4 = self._hut4.hut_health()
        h5 = self._hut5.hut_health()
        c1 = self._cannon1.can_health()
        c2 = self._cannon2.can_health()
        town = self._town.get_health()
        self._listh = [h1, h2, h3, h4, h5, c1, c2, town]
        pos, size, height, width, maxsize, health_val, damage = self._barcher1.get_dimension()
        wall_health = self._wall_down.wall_health()
        wall_health_up = self._wall_up.wall_health()
        can1 = self._cannon1.can_health()
        can2 = self._cannon2.can_health()

        # print("wall health:",wall_hea
        # lth,end=" ")
        mm = 10000
        index = 10
        for i in range(7):

            if(self._listh[i] > 0):

                dif = abs(self._listx[i]-pos[0])+abs(self._listy[i]-pos[1])
                if(dif < mm):
                    mm = dif
                    index = i
        if((wall_health > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6))) and ((pos[1]+1 == (int(self._height/2) - 5+10)) or (pos[1]-1 == (int(self._height/2) - 5+10)))):
            self._wall_down.update_health(damage)
            #
        elif(((wall_health_up > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6)))) and (((pos[1]+1 == (int(self._height/2) - 5)) or (pos[1]-1 == (int(self._height/2) - 5))))):
            self._wall_up.update_health(damage)

        elif((can1 > 0) and (((pos[0]+2 == 56) and pos[1] == 7) or (pos[0]-2 == 56 and pos[1] == 7) or (pos[1]+2 == 7 and pos[0] == 56) or (pos[1]-2 == 7 and pos[0] == 56))):
            self._cannon1.update_health(damage)

        elif((can2 > 0) and (((pos[0]+2 == 120) and pos[1] == 23) or (pos[0]-2 == 120 and pos[1] == 23) or (pos[1]+2 == 23 and pos[0] == 120) or (pos[1]-2 == 23 and pos[0] == 120))):
            self._cannon2.update_health(damage)
        else:

            # print("destyination:",self._listx[index],self._listy[ index],"index",index,end=" ")
            if(index != 10 and self._listx[index] > pos[0] and self._listx[index] != pos[0]):
                pos[0] += 1
            elif (index != 10 and self._listx[index] < pos[0] and self._listx[index] != pos[0]):
                pos[0] -= 1
            elif(index != 10 and self._listy[index] > pos[1] and self._listy[index]-5 != pos[1] and self._listx[index] == pos[0]):
                pos[1] += 1
            elif (index != 10 and self._listy[index] < pos[1] and self._listy[index]+5 != pos[1] and self._listx[index] == pos[0]):
                pos[1] -= 1
            else:
                if(index == 0):
                    self._hut1.update_health(damage)

                    if(self._hut1.hut_health() == 0):

                        mm = 10000

                        # self.barbarian_attack1()
                if(index == 1):

                    self._hut2.update_health(damage)
                    if(self._hut2.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 2):

                    self._hut3.update_health(damage)
                    if(self._hut3.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 3):

                    self._hut4.update_health(damage)
                    if(self._hut4.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 4):

                    self._hut5.update_health(damage)
                    if(self._hut5.hut_health() == 0):
                        mm = 10000
                if(index == 5):
                    self._cannon1.update_health(damage)
                    if(self._cannon1.can_health() == 0):
                        mm = 10000
                if(index == 6):
                    self._cannon2.update_health(damage)
                    if(self._cannon2.can_health() == 0):
                        mm = 10000
                if(index == 7):
                    self._town.update_health(damage)
                    if(self._town.get_health() == 0):
                        mm = 10000
    def archer_attackm2(self):
        h1 = self._hut1.hut_health()
        h2 = self._hut2.hut_health()
        h3 = self._hut3.hut_health()
        h4 = self._hut4.hut_health()
        h5 = self._hut5.hut_health()
        c1 = self._cannon1.can_health()
        c2 = self._cannon2.can_health()
        town = self._town.get_health()
        self._listh = [h1, h2, h3, h4, h5, c1, c2, town]
        pos, size, height, width, maxsize, health_val, damage = self._archer2.get_dimension()
        wall_health = self._wall_down.wall_health()
        wall_health_up = self._wall_up.wall_health()
        can1 = self._cannon1.can_health()
        can2 = self._cannon2.can_health()

        # print("wall health:",wall_hea
        # lth,end=" ")
        mm = 10000
        index = 10
        for i in range(7):

            if(self._listh[i] > 0):

                dif = abs(self._listx[i]-pos[0])+abs(self._listy[i]-pos[1])
                if(dif < mm):
                    mm = dif
                    index = i
        if((wall_health > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6))) and ((pos[1]+1 == (int(self._height/2) - 5+10)) or (pos[1]-1 == (int(self._height/2) - 5+10)))):
            self._wall_down.update_health(damage)
            #
        elif(((wall_health_up > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6)))) and (((pos[1]+1 == (int(self._height/2) - 5)) or (pos[1]-1 == (int(self._height/2) - 5))))):
            self._wall_up.update_health(damage)

        elif((can1 > 0) and (((pos[0]+2 == 56) and pos[1] == 7) or (pos[0]-2 == 56 and pos[1] == 7) or (pos[1]+2 == 7 and pos[0] == 56) or (pos[1]-2 == 7 and pos[0] == 56))):
            self._cannon1.update_health(damage)

        elif((can2 > 0) and (((pos[0]+2 == 120) and pos[1] == 23) or (pos[0]-2 == 120 and pos[1] == 23) or (pos[1]+2 == 23 and pos[0] == 120) or (pos[1]-2 == 23 and pos[0] == 120))):
            self._cannon2.update_health(damage)
        else:

            # print("destyination:",self._listx[index],self._listy[ index],"index",index,end=" ")
            if(index != 10 and self._listx[index] > pos[0] and self._listx[index] != pos[0]):
                pos[0] += 1
            elif (index != 10 and self._listx[index] < pos[0] and self._listx[index] != pos[0]):
                pos[0] -= 1
            elif(index != 10 and self._listy[index] > pos[1] and self._listy[index]-5 != pos[1] and self._listx[index] == pos[0]):
                pos[1] += 1
            elif (index != 10 and self._listy[index] < pos[1] and self._listy[index]+5 != pos[1] and self._listx[index] == pos[0]):
                pos[1] -= 1
            else:
                if(index == 0):
                    self._hut1.update_health(damage)

                    if(self._hut1.hut_health() == 0):

                        mm = 10000

                        # self.barbarian_attack1()
                if(index == 1):

                    self._hut2.update_health(damage)
                    if(self._hut2.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 2):

                    self._hut3.update_health(damage)
                    if(self._hut3.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 3):

                    self._hut4.update_health(damage)
                    if(self._hut4.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 4):

                    self._hut5.update_health(damage)
                    if(self._hut5.hut_health() == 0):
                        mm = 10000
                if(index == 5):
                    self._cannon1.update_health(damage)
                    if(self._cannon1.can_health() == 0):
                        mm = 10000
                if(index == 6):
                    self._cannon2.update_health(damage)
                    if(self._cannon2.can_health() == 0):
                        mm = 10000
                if(index == 7):
                    self._town.update_health(damage)
                    if(self._town.get_health() == 0):
                        mm = 10000
    def archer_attackm1(self):
        h1 = self._hut1.hut_health()
        h2 = self._hut2.hut_health()
        h3 = self._hut3.hut_health()
        h4 = self._hut4.hut_health()
        h5 = self._hut5.hut_health()
        c1 = self._cannon1.can_health()
        c2 = self._cannon2.can_health()
        town = self._town.get_health()
        self._listh = [h1, h2, h3, h4, h5, c1, c2, town]
        pos, size, height, width, maxsize, health_val, damage = self._archer1.get_dimension()
        wall_health = self._wall_down.wall_health()
        wall_health_up = self._wall_up.wall_health()
        can1 = self._cannon1.can_health()
        can2 = self._cannon2.can_health()

        # print("wall health:",wall_hea
        # lth,end=" ")
        mm = 10000
        index = 10
        for i in range(7):

            if(self._listh[i] > 0):

                dif = abs(self._listx[i]-pos[0])+abs(self._listy[i]-pos[1])
                if(dif < mm):
                    mm = dif
                    index = i
        if((wall_health > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6))) and ((pos[1]+1 == (int(self._height/2) - 5+10)) or (pos[1]-1 == (int(self._height/2) - 5+10)))):
            self._wall_down.update_health(damage)
            #
        elif(((wall_health_up > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6)))) and (((pos[1]+1 == (int(self._height/2) - 5)) or (pos[1]-1 == (int(self._height/2) - 5))))):
            self._wall_up.update_health(damage)

        elif((can1 > 0) and (((pos[0]+2 == 56) and pos[1] == 7) or (pos[0]-2 == 56 and pos[1] == 7) or (pos[1]+2 == 7 and pos[0] == 56) or (pos[1]-2 == 7 and pos[0] == 56))):
            self._cannon1.update_health(damage)

        elif((can2 > 0) and (((pos[0]+2 == 120) and pos[1] == 23) or (pos[0]-2 == 120 and pos[1] == 23) or (pos[1]+2 == 23 and pos[0] == 120) or (pos[1]-2 == 23 and pos[0] == 120))):
            self._cannon2.update_health(damage)
        else:

            # print("destyination:",self._listx[index],self._listy[ index],"index",index,end=" ")
            if(index != 10 and self._listx[index] > pos[0] and self._listx[index] != pos[0]):
                pos[0] += 1
            elif (index != 10 and self._listx[index] < pos[0] and self._listx[index] != pos[0]):
                pos[0] -= 1
            elif(index != 10 and self._listy[index] > pos[1] and self._listy[index]-5 != pos[1] and self._listx[index] == pos[0]):
                pos[1] += 1
            elif (index != 10 and self._listy[index] < pos[1] and self._listy[index]+5 != pos[1] and self._listx[index] == pos[0]):
                pos[1] -= 1
            else:
                if(index == 0):
                    self._hut1.update_health(damage)

                    if(self._hut1.hut_health() == 0):

                        mm = 10000

                        # self.barbarian_attack1()
                if(index == 1):

                    self._hut2.update_health(damage)
                    if(self._hut2.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 2):

                    self._hut3.update_health(damage)
                    if(self._hut3.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 3):

                    self._hut4.update_health(damage)
                    if(self._hut4.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 4):

                    self._hut5.update_health(damage)
                    if(self._hut5.hut_health() == 0):
                        mm = 10000
                if(index == 5):
                    self._cannon1.update_health(damage)
                    if(self._cannon1.can_health() == 0):
                        mm = 10000
                if(index == 6):
                    self._cannon2.update_health(damage)
                    if(self._cannon2.can_health() == 0):
                        mm = 10000
                if(index == 7):
                    self._town.update_health(damage)
                    if(self._town.get_health() == 0):
                        mm = 10000
    def king_sword_attck(self):
        pos, size, height, width, maxsize, health_val, damage = self._king.get_dimension()
        post, sizet, heightt, widtht, maxsizet, health_valt, damaget = self._town.get_dimension()
        posh1, sizeh1, heighth1, widthh1, maxsizeh1, health_valh1, damageh1 = self._hut1.get_dimension()
        posh2, sizeh2, heighth2, widthh2, maxsizeh2, health_valh2, damageh2 = self._hut2.get_dimension()
        posh3, sizeh3, heighth3, widthh3, maxsizeh3, health_valh3, damageh3 = self._hut3.get_dimension()
        posh4, sizeh4, heighth4, widthh4, maxsizeh4, health_valh4, damageh4 = self._hut4.get_dimension()       
        posh5, sizeh5, heighth5, widthh5, maxsizeh5, health_valh5, damageh5 = self._hut5.get_dimension()
        posc1, sizeh5, heighth5, widthh5, maxsizeh5, health_valh5, damageh5 = self._cannon1.get_dimension()
        posc2, sizeh5, heighth5, widthh5, maxsizeh5, health_valh5, damageh5 = self._cannon2.get_dimension()
        if(health_val > 0):
            if(post[0] >= (health_val > 0 and pos[0]-5) and (post[0] <= (pos[0]+5)) and (post[1] >= (pos[1]-5) and (post[1] <= (pos[1]+5)))):
                self._town.update_health(damage)
            if(posh1[0] >= (health_val > 0 and pos[0]-5) and (posh1[0] <= (pos[0]+5)) and (posh1[1] >= (pos[1]-5) and (posh1[1] <= (pos[1]+5)))):
                self._hut1.update_health(damage)
            if(posh2[0] >= (health_val > 0 and pos[0]-5) and (posh2[0] <= (pos[0]+5)) and (posh2[1] >= (pos[1]-5) and (posh2[1] <= (pos[1]+5)))):
                self._hut2.update_health(damage)
            if(posh3[0] >= (health_val > 0 and pos[0]-5) and (posh3[0] <= (pos[0]+5)) and (posh3[1] >= (pos[1]-5) and (posh3[1] <= (pos[1]+5)))):
                self._hut3.update_health(damage)
            if(posh4[0] >= (health_val > 0 and pos[0]-5) and (posh4[0] <= (pos[0]+5)) and (posh4[1] >= (pos[1]-5) and (posh4[1] <= (pos[1]+5)))):
                self._hut4.update_health(damage)
            if(posh5[0] >= (health_val > 0 and pos[0]-5) and (posh5[0] <= (pos[0]+5)) and (posh5[1] >= (pos[1]-5) and (posh5[1] <= (pos[1]+5)))):
                self._hut5.update_health(damage)
            if(posc1[0] >= (health_val > 0 and pos[0]-5) and (posc1[0] <= (pos[0]+5)) and (posc1[1] >= (pos[1]-5) and (posc1[1] <= (pos[1]+5)))):
                self._cannon1.update_health(damage)    
            if(posc2[0] >= (health_val > 0 and pos[0]-5) and (posc2[0] <= (pos[0]+5)) and (posc2[1] >= (pos[1]-5) and (posc2[1] <= (pos[1]+5)))):
                self._cannon2.update_health(damage)
               
    def barbarian_attackp1(self):
        h1 = self._hut1.hut_health()
        h2 = self._hut2.hut_health()
        h3 = self._hut3.hut_health()
        h4 = self._hut4.hut_health()
        h5 = self._hut5.hut_health()
        c1 = self._cannon1.can_health()
        c2 = self._cannon2.can_health()
        town = self._town.get_health()
        self._listh = [h1, h2, h3, h4, h5, c1, c2, town]
        pos, size, height, width, maxsize, health_val, damage = self._barbarian_p.get_dimension()
        wall_health = self._wall_down.wall_health()
        wall_health_up = self._wall_up.wall_health()
        can1 = self._cannon1.can_health()
        can2 = self._cannon2.can_health()

        # print("wall health:",wall_hea
        # lth,end=" ")
        mm = 10000
        index = 10
        for i in range(7):

            if(self._listh[i] > 0):

                dif = abs(self._listx[i]-pos[0])+abs(self._listy[i]-pos[1])
                if(dif < mm):
                    mm = dif
                    index = i
        if((wall_health > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6))) and ((pos[1]+1 == (int(self._height/2) - 5+10)) or (pos[1]-1 == (int(self._height/2) - 5+10)))):
            self._wall_down.update_health(damage)
            #
        elif(((wall_health_up > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6)))) and (((pos[1]+1 == (int(self._height/2) - 5)) or (pos[1]-1 == (int(self._height/2) - 5))))):
            self._wall_up.update_health(damage)

        elif((can1 > 0) and (((pos[0]+2 == 56) and pos[1] == 7) or (pos[0]-2 == 56 and pos[1] == 7) or (pos[1]+2 == 7 and pos[0] == 56) or (pos[1]-2 == 7 and pos[0] == 56))):
            self._cannon1.update_health(damage)

        elif((can2 > 0) and (((pos[0]+2 == 120) and pos[1] == 23) or (pos[0]-2 == 120 and pos[1] == 23) or (pos[1]+2 == 23 and pos[0] == 120) or (pos[1]-2 == 23 and pos[0] == 120))):
            self._cannon2.update_health(damage)
        else:

            # print("destyination:",self._listx[index],self._listy[ index],"index",index,end=" ")
            if(index != 10 and self._listx[index] > pos[0] and self._listx[index] != pos[0]):
                pos[0] += 1
            elif (index != 10 and self._listx[index] < pos[0] and self._listx[index] != pos[0]):
                pos[0] -= 1
            elif(index != 10 and self._listy[index] > pos[1] and self._listy[index]-1 != pos[1] and self._listx[index] == pos[0]):
                pos[1] += 1
            elif (index != 10 and self._listy[index] < pos[1] and self._listy[index]+1 != pos[1] and self._listx[index] == pos[0]):
                pos[1] -= 1
            else:
                if(index == 0):
                    self._hut1.update_health(damage)

                    if(self._hut1.hut_health() == 0):

                        mm = 10000

                        # self.barbarian_attack1()
                if(index == 1):

                    self._hut2.update_health(damage)
                    if(self._hut2.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 2):

                    self._hut3.update_health(damage)
                    if(self._hut3.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 3):

                    self._hut4.update_health(damage)
                    if(self._hut4.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 4):

                    self._hut5.update_health(damage)
                    if(self._hut5.hut_health() == 0):
                        mm = 10000
                if(index == 5):
                    self._cannon1.update_health(damage)
                    if(self._cannon1.can_health() == 0):
                        mm = 10000
                if(index == 6):
                    self._cannon2.update_health(damage)
                    if(self._cannon2.can_health() == 0):
                        mm = 10000
                if(index == 7):
                    self._town.update_health(damage)
                    if(self._town.get_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()

    def barbarian_attackp2(self):
        h1 = self._hut1.hut_health()
        h2 = self._hut2.hut_health()
        h3 = self._hut3.hut_health()
        h4 = self._hut4.hut_health()
        h5 = self._hut5.hut_health()
        c1 = self._cannon1.can_health()
        c2 = self._cannon2.can_health()
        town = self._town.get_health()
        self._listh = [h1, h2, h3, h4, h5, c1, c2, town]
        pos, size, height, width, maxsize, health_val, damage = self._barbarian_p1.get_dimension()
        wall_health = self._wall_down.wall_health()
        wall_health_up = self._wall_up.wall_health()
        can1 = self._cannon1.can_health()
        can2 = self._cannon2.can_health()
        mm = 10000
        index = 10

        for i in range(7):

            if(self._listh[i] > 0):

                dif = abs(self._listx[i]-pos[0])+abs(self._listy[i]-pos[1])
                if(dif < mm):
                    mm = dif
                    index = i
        # print(pos[0], pos[1], self._listx[index], self._listy[index])
        if((wall_health > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6))) and ((pos[1]+1 == (int(self._height/2) - 5+10)) or (pos[1]-1 == (int(self._height/2) - 5+10)))):
            self._wall_down.update_health(damage)
        elif(((wall_health_up > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6)))) and (((pos[1]+1 == (int(self._height/2) - 5)) or (pos[1]-1 == (int(self._height/2) - 5))))):

            self._wall_up.update_health(damage)

        elif((can1 > 0) and (((pos[0]+2 == 56) and pos[1] == 7) or (pos[0]-2 == 56 and pos[1] == 7) or (pos[1]+2 == 7 and pos[0] == 56) or (pos[1]-2 == 7 and pos[0] == 56))):
            self._cannon1.update_health(damage)

        elif((can2 > 0) and (((pos[0]+2 == 120) and pos[1] == 23) or (pos[0]-2 == 120 and pos[1] == 23) or (pos[1]+2 == 23 and pos[0] == 120) or (pos[1]-2 == 23 and pos[0] == 120))):
            self._cannon2.update_health(damage)
        else:

            # print("destyination:",self._listx[index],self._listy[ index],"index",index,end=" ")
            if(index != 10 and self._listx[index] > pos[0] and self._listx[index] != pos[0]):
                pos[0] += 1
            elif (index != 10 and self._listx[index] < pos[0] and self._listx[index] != pos[0]):
                pos[0] -= 1
            elif(index != 10 and self._listy[index] > pos[1] and self._listy[index]-1 != pos[1] and self._listx[index] == pos[0]):
                pos[1] += 1
            elif (index != 10 and self._listy[index] < pos[1] and self._listy[index]+1 != pos[1] and self._listx[index] == pos[0]):
                pos[1] -= 1
            else:
                if(index == 0):
                    self._hut1.update_health(damage)

                    if(self._hut1.hut_health() == 0):

                        mm = 10000

                        # self.barbarian_attack1()
                if(index == 1):

                    self._hut2.update_health(damage)
                    if(self._hut2.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 2):

                    self._hut3.update_health(damage)
                    if(self._hut3.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 3):

                    self._hut4.update_health(damage)
                    if(self._hut4.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 4):

                    self._hut5.update_health(damage)
                    if(self._hut5.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 5):
                    self._cannon1.update_health(damage)
                    if(self._cannon1.can_health() == 0):
                        mm = 10000
                if(index == 6):
                    self._cannon2.update_health(damage)
                    if(self._cannon2.can_health() == 0):
                        mm = 10000
                if(index == 7):
                    self._town.update_health(damage)
                    if(self._town.get_health() == 0):
                        mm = 10000

    def barbarian_attackp3(self):
        h1 = self._hut1.hut_health()
        h2 = self._hut2.hut_health()
        h3 = self._hut3.hut_health()
        h4 = self._hut4.hut_health()
        h5 = self._hut5.hut_health()
        c1= self._cannon1.can_health()
        c2 = self._cannon2.can_health()
        town = self._town.get_health()
        self._listh = [h1, h2, h3, h4, h5,c1,c2,town]
        pos, size, height, width, maxsize, health_val, damage = self._barbarian_p2.get_dimension()
        wall_health_down = self._wall_down.wall_health()
        wall_health_up = self._wall_up.wall_health()
        can1 = self._cannon1.can_health()
        can2 = self._cannon2.can_health()
        # print("wall health:",wall_health,end=" ")
        mm = 10000
        index = 10
        for i in range(7):

            if(self._listh[i] > 0):

                dif = abs(self._listx[i]-pos[0])+abs(self._listy[i]-pos[1])
                if(dif < mm):
                    mm = dif
                    index = i
        if((wall_health_down > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6))) and ((pos[1]+1 == (int(self._height/2) - 5+10)) or (pos[1]-1 == (int(self._height/2) - 5+10)))):
            self._wall_down.update_health(damage)
            # 
        elif(((wall_health_up > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6)))) and (((pos[1]+1 == (int(self._height/2) - 5)) or (pos[1]-1 == (int(self._height/2) - 5))))):
            self._wall_up.update_health(damage)
        elif((can1 > 0) and (((pos[0]+2 == 56) and pos[1] == 7) or (pos[0]-2 == 56 and pos[1] == 7) or (pos[1]+2 == 7 and pos[0] == 56) or (pos[1]-2 == 7 and pos[0] == 56))):
            self._cannon1.update_health(damage)

        elif((can2 > 0) and (((pos[0]+2 == 120) and pos[1] == 23) or (pos[0]-2 == 120 and pos[1] == 23) or (pos[1]+2 == 23 and pos[0] == 120) or (pos[1]-2 == 23 and pos[0] == 120))):
            self._cannon2.update_health(damage)
        else:

            # print("destyination:",self._listx[index],self._listy[ index],"index",index,end=" ")
            if(index != 10 and self._listx[index] > pos[0] and self._listx[index] != pos[0]):
                pos[0] += 1
            elif (index != 10 and self._listx[index] < pos[0] and self._listx[index] != pos[0]):
                pos[0] -= 1
            elif(index != 10 and self._listy[index] > pos[1] and self._listy[index]-1 != pos[1] and self._listx[index] == pos[0]):
                pos[1] += 1
            elif (index != 10 and self._listy[index] < pos[1] and self._listy[index]+1 != pos[1] and self._listx[index] == pos[0]):
                pos[1] -= 1
            else:
                if(index == 0):
                    self._hut1.update_health(damage)

                    if(self._hut1.hut_health() == 0):

                        mm = 10000
                        
                        # self.barbarian_attack1()
                if(index == 1):

                    self._hut2.update_health(damage)
                    if(self._hut2.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 2):

                    self._hut3.update_health(damage)
                    if(self._hut3.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 3):

                    self._hut4.update_health(damage)
                    if(self._hut4.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 4):

                    self._hut5.update_health(damage)
                    if(self._hut5.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 5):
                    self._cannon1.update_health(damage)
                    if(self._cannon1.can_health() == 0):
                        mm = 10000
                if(index == 6):
                    self._cannon2.update_health(damage)
                    if(self._cannon2.can_health() == 0):
                        mm = 10000
                if(index == 7):
                    self._town.update_health(damage)
                    if(self._town.get_health() == 0):
                        mm = 10000
                        
    def barbarian_attackj1(self):
        h1 = self._hut1.hut_health()
        h2 = self._hut2.hut_health()
        h3 = self._hut3.hut_health()
        h4 = self._hut4.hut_health()
        h5 = self._hut5.hut_health()
        c1= self._cannon1.can_health()
        c2 = self._cannon2.can_health()
        town = self._town.get_health()
        self._listh = [h1, h2, h3, h4, h5,c1,c2,town]
        pos, size, height, width, maxsize, health_val, damage = self._barbarian_k.get_dimension()
        wall_health = self._wall_down.wall_health()
        wall_health_up = self._wall_up.wall_health()
        can1 = self._cannon1.can_health()
        can2 = self._cannon2.can_health()
        # print("wall health:",wall_health,end=" ")
        mm = 10000
        index = 10
        for i in range(7):

            if(self._listh[i] > 0):

                dif = abs(self._listx[i]-pos[0])+abs(self._listy[i]-pos[1])
                if(dif < mm):
                    mm = dif
                    index = i
        if((wall_health > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6))) and ((pos[1]+1 == (int(self._height/2) - 5+10)) or (pos[1]-1 == (int(self._height/2) - 5+10)))):
            self._wall_down.update_health(damage)
            # 
        elif(((wall_health_up > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6)))) and (((pos[1]+1 == (int(self._height/2) - 5)) or (pos[1]-1 == (int(self._height/2) - 5))))):
            self._wall_up.update_health(damage)
        elif((can1 > 0) and (((pos[0]+2 == 56) and pos[1] == 7) or (pos[0]-2 == 56 and pos[1] == 7) or (pos[1]+2 == 7 and pos[0] == 56) or (pos[1]-2 == 7 and pos[0] == 56))):
            self._cannon1.update_health(damage)

        elif((can2 > 0) and (((pos[0]+2 == 120) and pos[1] == 23) or (pos[0]-2 == 120 and pos[1] == 23) or (pos[1]+2 == 23 and pos[0] == 120) or (pos[1]-2 == 23 and pos[0] == 120))):
            self._cannon2.update_health(damage)
        else:

            # print("destyination:",self._listx[index],self._listy[ index],"index",index,end=" ")
            if(index != 10 and self._listx[index] > pos[0] and self._listx[index] != pos[0]):
                pos[0] += 1
            elif (index != 10 and self._listx[index] < pos[0] and self._listx[index] != pos[0]):
                pos[0] -= 1
            elif(index != 10 and self._listy[index] > pos[1] and self._listy[index]-1 != pos[1] and self._listx[index] == pos[0]):
                pos[1] += 1
            elif (index != 10 and self._listy[index] < pos[1] and self._listy[index]+1 != pos[1] and self._listx[index] == pos[0]):
                pos[1] -= 1
            else:
                if(index == 0):
                    self._hut1.update_health(damage)

                    if(self._hut1.hut_health() == 0):

                        mm = 10000
                        
                        # self.barbarian_attack1()
                if(index == 1):

                    self._hut2.update_health(damage)
                    if(self._hut2.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 2):

                    self._hut3.update_health(damage)
                    if(self._hut3.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 3):

                    self._hut4.update_health(damage)
                    if(self._hut4.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 4):

                    self._hut5.update_health(damage)
                    if(self._hut5.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 5):
                    self._cannon1.update_health(damage)
                    if(self._cannon1.can_health() == 0):
                        mm = 10000
                if(index == 6):
                    self._cannon2.update_health(damage)
                    if(self._cannon2.can_health() == 0):
                        mm = 10000
                if(index == 7):
                    self._town.update_health(damage)
                    if(self._town.get_health() == 0):
                        mm = 10000

    def barbarian_attackj2(self):
        h1 = self._hut1.hut_health()
        h2 = self._hut2.hut_health()
        h3 = self._hut3.hut_health()
        h4 = self._hut4.hut_health()
        h5 = self._hut5.hut_health()
        c1= self._cannon1.can_health()
        c2 = self._cannon2.can_health()
        town = self._town.get_health()
        self._listh = [h1, h2, h3, h4, h5,c1,c2,town]
        pos, size, height, width, maxsize, health_val, damage = self._barbarian_k1.get_dimension()
        wall_health = self._wall_down.wall_health()
        wall_health_up = self._wall_up.wall_health()
        can1 = self._cannon1.can_health()
        can2 = self._cannon2.can_health()
        mm = 10000
        index = 10
        for i in range(7):

            if(self._listh[i] > 0):

                dif = abs(self._listx[i]-pos[0])+abs(self._listy[i]-pos[1])
                if(dif < mm):
                    mm = dif
                    index = i
        if((wall_health > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6))) and ((pos[1]+1 == (int(self._height/2) - 5+10)) or (pos[1]-1 == (int(self._height/2) - 5+10)))):
            self._wall_down.update_health(damage)
        elif(((wall_health_up > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6)))) and (((pos[1]+1 == (int(self._height/2) - 5)) or (pos[1]-1 == (int(self._height/2) - 5))))):

            self._wall_up.update_health(damage)  
        elif((can1 > 0) and (((pos[0]+2 == 56) and pos[1] == 7) or (pos[0]-2 == 56 and pos[1] == 7) or (pos[1]+2 == 7 and pos[0] == 56) or (pos[1]-2 == 7 and pos[0] == 56))):
            self._cannon1.update_health(damage)

        elif((can2 > 0) and (((pos[0]+2 == 120) and pos[1] == 23) or (pos[0]-2 == 120 and pos[1] == 23) or (pos[1]+2 == 23 and pos[0] == 120) or (pos[1]-2 == 23 and pos[0] == 120))):
            self._cannon2.update_health(damage) 
        else:

            # print("destyination:",self._listx[index],self._listy[ index],"index",index,end=" ")
            if(index != 10 and self._listx[index] > pos[0] and self._listx[index] != pos[0]):
                pos[0] += 1
            elif (index != 10 and self._listx[index] < pos[0] and self._listx[index] != pos[0]):
                pos[0] -= 1
            elif(index != 10 and self._listy[index] > pos[1] and self._listy[index]-1 != pos[1] and self._listx[index] == pos[0]):
                pos[1] += 1
            elif (index != 10 and self._listy[index] < pos[1] and self._listy[index]+1 != pos[1] and self._listx[index] == pos[0]):
                pos[1] -= 1
            else:
                if(index == 0):
                    self._hut1.update_health(damage)

                    if(self._hut1.hut_health() == 0):

                        mm = 10000
                        
                        # self.barbarian_attack1()
                if(index == 1):

                    self._hut2.update_health(damage)
                    if(self._hut2.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 2):

                    self._hut3.update_health(damage)
                    if(self._hut3.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 3):

                    self._hut4.update_health(damage)
                    if(self._hut4.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 4):

                    self._hut5.update_health(damage)
                    if(self._hut5.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 5):
                    self._cannon1.update_health(damage)
                    if(self._cannon1.can_health() == 0):
                        mm = 10000
                if(index == 6):
                    self._cannon2.update_health(damage)
                    if(self._cannon2.can_health() == 0):
                        mm = 10000
                if(index == 7):
                    self._town.update_health(damage)
                    if(self._town.get_health() == 0):
                        mm = 10000


    def barbarian_attackj3(self):
        h1 = self._hut1.hut_health()
        h2 = self._hut2.hut_health()
        h3 = self._hut3.hut_health()
        h4 = self._hut4.hut_health()
        h5 = self._hut5.hut_health()
        c1= self._cannon1.can_health()
        c2 = self._cannon2.can_health()
        town = self._town.get_health()
        self._listh = [h1, h2, h3, h4, h5,c1,c2,town]
        pos, size, height, width, maxsize, health_val, damage = self._barbarian_k2.get_dimension()
        wall_health_down = self._wall_down.wall_health()
        wall_health_up = self._wall_up.wall_health()
        # print("wall health:",wall_health,end=" ")
        can1 = self._cannon1.can_health()
        can2 = self._cannon2.can_health()
        mm = 10000
        index = 10
        for i in range(7):

            if(self._listh[i] > 0):

                dif = abs(self._listx[i]-pos[0])+abs(self._listy[i]-pos[1])
                if(dif < mm):
                    mm = dif
                    index = i
        if((wall_health_down > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6))) and ((pos[1]+1 == (int(self._height/2) - 5+10)) or (pos[1]-1 == (int(self._height/2) - 5+10)))):
            self._wall_down.update_health(damage)
            # 
        elif(((wall_health_up > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6)))) and (((pos[1]+1 == (int(self._height/2) - 5)) or (pos[1]-1 == (int(self._height/2) - 5))))):
            self._wall_up.update_health(damage)
        elif((can1 > 0) and (((pos[0]+2 == 56) and pos[1] == 7) or (pos[0]-2 == 56 and pos[1] == 7) or (pos[1]+2 == 7 and pos[0] == 56) or (pos[1]-2 == 7 and pos[0] == 56))):
            self._cannon1.update_health(damage)

        elif((can2 > 0) and (((pos[0]+2 == 120) and pos[1] == 23) or (pos[0]-2 == 120 and pos[1] == 23) or (pos[1]+2 == 23 and pos[0] == 120) or (pos[1]-2 == 23 and pos[0] == 120))):
            self._cannon2.update_health(damage) 
        else:

            # print("destyination:",self._listx[index],self._listy[ index],"index",index,end=" ")
            if(index != 10 and self._listx[index] > pos[0] and self._listx[index] != pos[0]):
                pos[0] += 1
            elif (index != 10 and self._listx[index] < pos[0] and self._listx[index] != pos[0]):
                pos[0] -= 1
            elif(index != 10 and self._listy[index] > pos[1] and self._listy[index]-1 != pos[1] and self._listx[index] == pos[0]):
                pos[1] += 1
            elif (index != 10 and self._listy[index] < pos[1] and self._listy[index]+1 != pos[1] and self._listx[index] == pos[0]):
                pos[1] -= 1
            else:
                if(index == 0):
                    self._hut1.update_health(damage)

                    if(self._hut1.hut_health() == 0):

                        mm = 10000
                        
                        # self.barbarian_attack1()
                if(index == 1):

                    self._hut2.update_health(damage)
                    if(self._hut2.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 2):

                    self._hut3.update_health(damage)
                    if(self._hut3.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 3):

                    self._hut4.update_health(damage)
                    if(self._hut4.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 4):

                    self._hut5.update_health(damage)
                    if(self._hut5.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                        
                if(index == 5):
                    self._cannon1.update_health(damage)
                    if(self._cannon1.can_health() == 0):
                        mm = 10000
                if(index == 6):
                    self._cannon2.update_health(damage)
                    if(self._cannon2.can_health() == 0):
                        mm = 10000
                if(index == 7):
                    self._town.update_health(damage)
                    if(self._town.get_health() == 0):
                        mm = 10000

    def barbarian_attackl1(self):
        h1 = self._hut1.hut_health()
        h2 = self._hut2.hut_health()
        h3 = self._hut3.hut_health()
        h4 = self._hut4.hut_health()
        h5 = self._hut5.hut_health()
        c1= self._cannon1.can_health()
        c2 = self._cannon2.can_health()
        town = self._town.get_health()
        self._listh = [h1, h2, h3, h4, h5,c1,c2,town]
        pos, size, height, width, maxsize, health_val, damage = self._barbarian_l.get_dimension()
        wall_health = self._wall_down.wall_health()
        wall_health_up = self._wall_up.wall_health()
        # print("wall health:",wall_health,end=" ")
        mm = 10000
        index = 10
        for i in range(7):

            if(self._listh[i] > 0):

                dif = abs(self._listx[i]-pos[0])+abs(self._listy[i]-pos[1])
                if(dif < mm):
                    mm = dif
                    index = i
        if((wall_health > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6))) and ((pos[1]+1 == (int(self._height/2) - 5+10)) or (pos[1]-1 == (int(self._height/2) - 5+10)))):
            self._wall_down.update_health(damage)
            # 
        elif(((wall_health_up > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6)))) and (((pos[1]+1 == (int(self._height/2) - 5)) or (pos[1]-1 == (int(self._height/2) - 5))))):
            self._wall_up.update_health(damage)
        else:

            # print("destyination:",self._listx[index],self._listy[ index],"index",index,end=" ")
            if(index != 10 and self._listx[index] > pos[0] and self._listx[index] != pos[0]):
                pos[0] += 1
            elif (index != 10 and self._listx[index] < pos[0] and self._listx[index] != pos[0]):
                pos[0] -= 1
            elif(index != 10 and self._listy[index] > pos[1] and self._listy[index]-1 != pos[1] and self._listx[index] == pos[0]):
                pos[1] += 1
            elif (index != 10 and self._listy[index] < pos[1] and self._listy[index]+1 != pos[1] and self._listx[index] == pos[0]):
                pos[1] -= 1
            else:
                if(index == 0):
                    self._hut1.update_health(damage)

                    if(self._hut1.hut_health() == 0):

                        mm = 10000
                        
                        # self.barbarian_attack1()
                if(index == 1):

                    self._hut2.update_health(damage)
                    if(self._hut2.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 2):

                    self._hut3.update_health(damage)
                    if(self._hut3.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 3):

                    self._hut4.update_health(damage)
                    if(self._hut4.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 4):

                    self._hut5.update_health(damage)
                    if(self._hut5.hut_health() == 0):
                        mm = 10000
                        
                if(index == 5):
                    self._cannon1.update_health(damage)
                    if(self._cannon1.can_health() == 0):
                        mm = 10000
                if(index == 6):
                    self._cannon2.update_health(damage)
                    if(self._cannon2.can_health() == 0):
                        mm = 10000
                if(index == 7):
                    self._town.update_health(damage)
                    if(self._town.get_health() == 0):
                        mm = 10000        # self.barbarian_attack1()

    def barbarian_attackl2(self):
        h1 = self._hut1.hut_health()
        h2 = self._hut2.hut_health()
        h3 = self._hut3.hut_health()
        h4 = self._hut4.hut_health()
        h5 = self._hut5.hut_health()
        c1= self._cannon1.can_health()
        c2 = self._cannon2.can_health()
        town = self._town.get_health()
        self._listh = [h1, h2, h3, h4, h5,c1,c2,town]
        pos, size, height, width, maxsize, health_val, damage = self._barbarian_l1.get_dimension()
        wall_health = self._wall_down.wall_health()
        wall_health_up = self._wall_up.wall_health()
        # print("wall health:",wall_health,end=" ")
        mm = 10000
        index = 10
        for i in range(7):

            if(self._listh[i] > 0):

                dif = abs(self._listx[i]-pos[0])+abs(self._listy[i]-pos[1])
                if(dif < mm):
                    mm = dif
                    index = i
        if((wall_health > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6))) and ((pos[1]+1 == (int(self._height/2) - 5+10)) or (pos[1]-1 == (int(self._height/2) - 5+10)))):
            self._wall_down.update_health(damage)
        elif(((wall_health_up > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6)))) and (((pos[1]+1 == (int(self._height/2) - 5)) or (pos[1]-1 == (int(self._height/2) - 5))))):

            self._wall_up.update_health(damage)     # 
        else:

            # print("destyination:",self._listx[index],self._listy[ index],"index",index,end=" ")
            if(index != 10 and self._listx[index] > pos[0] and self._listx[index] != pos[0]):
                pos[0] += 1
            elif (index != 10 and self._listx[index] < pos[0] and self._listx[index] != pos[0]):
                pos[0] -= 1
            elif(index != 10 and self._listy[index] > pos[1] and self._listy[index]-1 != pos[1] and self._listx[index] == pos[0]):
                pos[1] += 1
            elif (index != 10 and self._listy[index] < pos[1] and self._listy[index]+1 != pos[1] and self._listx[index] == pos[0]):
                pos[1] -= 1
            else:
                if(index == 0):
                    self._hut1.update_health(damage)

                    if(self._hut1.hut_health() == 0):

                        mm = 10000
                        
                        # self.barbarian_attack1()
                if(index == 1):

                    self._hut2.update_health(damage)
                    if(self._hut2.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 2):

                    self._hut3.update_health(damage)
                    if(self._hut3.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 3):

                    self._hut4.update_health(damage)
                    if(self._hut4.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 4):

                    self._hut5.update_health(damage)
                    if(self._hut5.hut_health() == 0):
                        mm = 10000
                        
                if(index == 5):
                    self._cannon1.update_health(damage)
                    if(self._cannon1.can_health() == 0):
                        mm = 10000
                if(index == 6):
                    self._cannon2.update_health(damage)
                    if(self._cannon2.can_health() == 0):
                        mm = 10000
                if(index == 7):
                    self._town.update_health(damage)
                    if(self._town.get_health() == 0):
                        mm = 10000        # self.barbarian_attack1()

    def barbarian_attackl3(self):
        h1 = self._hut1.hut_health()
        h2 = self._hut2.hut_health()
        h3 = self._hut3.hut_health()
        h4 = self._hut4.hut_health()
        h5 = self._hut5.hut_health()
        c1= self._cannon1.can_health()
        c2 = self._cannon2.can_health()
        town = self._town.get_health()
        self._listh = [h1, h2, h3, h4, h5,c1,c2,town]
        pos, size, height, width, maxsize, health_val, damage = self._barbarian_l2.get_dimension()
        wall_health_down = self._wall_down.wall_health()
        wall_health_up = self._wall_up.wall_health()
        # print("wall health:",wall_health,end=" ")
        mm = 10000
        index = 10
        for i in range(7):

            if(self._listh[i] > 0):

                dif = abs(self._listx[i]-pos[0])+abs(self._listy[i]-pos[1])
                if(dif < mm):
                    mm = dif
                    index = i
        if((wall_health_down > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6))) and ((pos[1]+1 == (int(self._height/2) - 5+10)) or (pos[1]-1 == (int(self._height/2) - 5+10)))):
            self._wall_down.update_health(damage)
            # 
        elif(((wall_health_up > 0) and (pos[0] <= (int(self._width/2)-6+18) and (pos[0] >= (int(self._width/2)-6)))) and (((pos[1]+1 == (int(self._height/2) - 5)) or (pos[1]-1 == (int(self._height/2) - 5))))):
            self._wall_up.update_health(damage)
        else:

            # print("destyination:",self._listx[index],self._listy[ index],"index",index,end=" ")
            if(index != 10 and self._listx[index] > pos[0] and self._listx[index] != pos[0]):
                pos[0] += 1
            elif (index != 10 and self._listx[index] < pos[0] and self._listx[index] != pos[0]):
                pos[0] -= 1
            elif(index != 10 and self._listy[index] > pos[1] and self._listy[index]-1 != pos[1] and self._listx[index] == pos[0]):
                pos[1] += 1
            elif (index != 10 and self._listy[index] < pos[1] and self._listy[index]+1 != pos[1] and self._listx[index] == pos[0]):
                pos[1] -= 1
            else:
                if(index == 0):
                    self._hut1.update_health(damage)

                    if(self._hut1.hut_health() == 0):

                        mm = 10000
                        
                        # self.barbarian_attack1()
                if(index == 1):

                    self._hut2.update_health(damage)
                    if(self._hut2.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 2):

                    self._hut3.update_health(damage)
                    if(self._hut3.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 3):

                    self._hut4.update_health(damage)
                    if(self._hut4.hut_health() == 0):
                        mm = 10000
                        # self.barbarian_attack1()
                if(index == 4):

                    self._hut5.update_health(damage)
                    if(self._hut5.hut_health() == 0):
                        mm = 10000
                        
                if(index == 5):
                    self._cannon1.update_health(damage)
                    if(self._cannon1.can_health() == 0):
                        mm = 10000
                if(index == 6):
                    self._cannon2.update_health(damage)
                    if(self._cannon2.can_health() == 0):
                        mm = 10000
                if(index == 7):
                    self._town.update_health(damage)
                    if(self._town.get_health() == 0):
                        mm = 10000        # self.barbarian_attack1()

    def key_board_interrupt(self):
        get = Get()
        ch = input_to(get.__call__)
        if(ch == 'q'):
            sys.exit()
        elif(ch == 'k'):
            if(self._queenval==0):
                self._kingval = 1
        elif(ch == 'o'):
            if(self._kingval==0):
                self._queenval = 1
        elif ch == 'd':
            if(self._kingval==1):
                self._king.move(ch)
            if(self._queenval==1):
                self._queen.move(ch)
        elif ch == 'a':
            if(self._kingval==1):
                self._king.move(ch)
            if(self._queenval==1):
                self._queen.move(ch)
        elif ch == 'w':
            if(self._kingval==1):
                self._king.move(ch)
            if(self._queenval==1):
                self._queen.move(ch)
        elif ch == 's':
            if(self._kingval==1):
                self._king.move(ch)
            if(self._queenval==1):
                self._queen.move(ch)
        elif ch == ' ':
            self._kingattack_falg = 1
            self._queenattack_falg = 1
        elif ch == 'p':
            self._pcounter += 1
        elif ch == 'm':
            self._mcounter += 1
        elif ch == 'n':
            self._ncounter += 1
        elif ch == 'b':
            self._bcounter += 1
        elif ch == 'v':
            self._vcounter += 1
        elif ch == 'c':
            self._ccounter += 1
        elif ch == 'x':
            self._xcounter += 1
        elif ch == 'j':
            self._kcounter += 1
        elif ch == 'l':
            self._lcounter += 1
        elif ch == 'x': # sword attack bonus continues press
            self.king_sword_attck()
        elif ch == 'r': # range spell
            if(self._king._health_val>0):
                self._king.range_spell()
            if(self._barbarian_p._health_val>0 and self._sp1==1):
                self._barbarian_p.range_spell()
            if(self._barbarian_p1._health_val>0 and self._sp2==1):
                self._barbarian_p1.range_spell()
            if(self._barbarian_l._health_val>0 and self._sl1==1):
                self._barbarian_l.range_spell()
            if(self._barbarian_l1._health_val>0 and self._sl2==1):
                self._barbarian_l1.range_spell()
            if(self._barbarian_l2._health_val>0 and self._sl3==1):
                self._barbarian_l2.range_spell()
            if(self._barbarian_k._health_val>0 and self._sk1==1):
                self._barbarian_k.range_spell()
            if(self._barbarian_k1._health_val>0 and self._sk2==1):
                self._barbarian_k1.range_spell()
            if(self._barbarian_k2._health_val>0 and self._sk3==1):
                self._barbarian_k2.range_spell()
            if(self._barbarian_p1._health_val>0 and self._sp2==1):
                self._barbarian_p1.range_spell()
        elif ch == 't': # Heal spell
            if(self._king._health_val>0):
                self._king.heal_spell()
            if(self._barbarian_p._health_val>0 and self._sp1==1):
                self._barbarian_p.heal_spell()
            if(self._barbarian_p1._health_val>0 and self._sp2==1):
                self._barbarian_p1.heal_spell()
            if(self._barbarian_l._health_val>0 and self._sl1==1):
                self._barbarian_l.heal_spell()
            if(self._barbarian_l1._health_val>0 and self._sl2==1):
                self._barbarian_l1.heal_spell()
            if(self._barbarian_l2._health_val>0 and self._sl3==1):
                self._barbarian_l2.heal_spell()
            if(self._barbarian_k._health_val>0 and self._sk1==1):
                self._barbarian_k.heal_spell()
            if(self._barbarian_k1._health_val>0 and self._sk2==1):
                self._barbarian_k1.heal_spell()
            if(self._barbarian_k2._health_val>0 and self._sk3==1):
                self._barbarian_k2.heal_spell()
            if(self._barbarian_p1._health_val>0 and self._sp2==1):
                self._barbarian_p1.heal_spell()
        return ch    

    def run(self):
        itteration = 0
        self.start()
        # f=open("replay/replay.txt","w")
        replay_number = open("replay/number.txt","r")
        number = replay_number.readlines()
        number_int = int (number[0])
        number_int = number_int+1
        f = open("replay/number.txt","w")
        f.write(str(number_int))
        replay = open("replay/"+str(number_int)+".txt","w")
        start_time=time.time()
        while True:
            self._screen.clean()
            self._screen.reset_screen()
            move=self.key_board_interrupt()
            curr_time=time.time()-start_time
            if(move!=None):
                replay.write("{} {}\n".format(move,itteration))
            if(self._kingval==1):
                self.king_attack()
            if(self._queenval==1):
                self.queen_attack()
            self.cannon_attack()
            self.wizard_attack()
            # self.Balloon_attack()
            # self.king_sword_attck()
            self.placing()
            self.result()

            self._screen.render_screen()
            itteration+=1

game = Game()
game.run()
