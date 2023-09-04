import sys
sys.path.insert(0, './src')
from cmath import sqrt, tan
from mimetypes import init
from operator import ipow
import os
import time
import numpy as np
from color import *
from objects import Barbarian, Cannon, Hut, Item, King, Wall
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
        # self._board = np.array([[''for j in range(self._width)]
        #                        for i in range(self._height)], dtype='object')

        self._board = np.zeros((self._height, self._width), dtype='object')
        for i in range(self._height):
            for j in range(self._width):
                self._board[i][j] = ''

        print("\033[2J")  # CLAERING SCREEN

    def clean(self):
        # self._board = np.array([[''for j in range(self._width)]
        #                        for i in range(self._height)], dtype='object')
        self._board = np.zeros((self._height, self._width), dtype='object')
        for i in range(self._height):
            for j in range(self._width):
                self._board[i][j] = ''
        # set screen to begining
        print("\033[0;0H")
        i = 0
        while i < self._height:
            # for i in range(self._height):
            j = 0
            while j < self._width:
                # for j in range(self._width):
                print(self._board[i][j], end='')
                j += 1
            print(" ")
            i += 1

    def render_screen(self):
        # set cursor to beginning
        print("\033[0;0H")

        # for i in range(self._height):
        i = 0
        while i < self._height:
            # for j in range(self._width):
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
            # for j in range(self._width):
            j = 0
            while j < self._width:
                # Top wall and bottom
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
        self._kingval = 1
        # self._leftx =[int(self._width/2)-6,]
        # self._lefty=[int(self._height/2) - 4,int(self._height/2) - 3,int(self._height/2) - 2,int(self._height/2) - 1,int(self._height/2) ,int(self._height/2)+1,int(self._height/2)+2,int(self._height/2)+3,int(self._height/2)+4]
        # self._rightx=[int(self._height/2) - 4,int(self._height/2) - 3,int(self._height/2) - 2,int(self._height/2) - 1,int(self._height/2) ,int(self._height/2) +1,int(self._height/2) +2,int(self._height/2) +3,int(self._height/2) +4]
        self._kingattack = 1
        self._sword =0
        self._kingattack_falg =0
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

        self._hut1 = Hut([int(12), int(3)], [1, 1], 1, 1, [
                         self._width, self._height], int(70), 0)
        self._hut2 = Hut([int((self._width/2)), int(3)], [1, 1],
                         1, 1, [self._width, self._height], int(100), 0)
        self._hut3 = Hut([int(28), int(20)], [1, 1], 1, 1, [
                         self._width, self._height], int(100), 0)
        self._hut4 = Hut([int((self._width-15)), int(3)], [1, 1],
                         1, 1, [self._width, self._height], int(100), 0)
        self._hut5 = Hut([int((self._width-15)), int(20)], [1, 1],
                         1, 1, [self._width, self._height], int(100), 0)
        self._cannon1 = Cannon([int(56), int(7)], [1, 1], 1, 0, [
                               self._width, self._height], int(100), 5)
        self._cannon2 = Cannon([int(120), int(23)], [1, 1], 1, 0, [
                               self._width, self._height], int(100), 5)

        self._listx = [12, int((self._width/2)), 28, int((self._width-15)),
                               int((self._width/2-15)), 56, 120, 56, 120, int(self._width/2)]
        self._listy = [3, 3, 20, 3, 20, 7, 23, (int(self._height/2))-2]

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
        j3 = self._barbarian_k2.item_pos()
        l1 = self._barbarian_l.item_pos()
        l2 = self._barbarian_l1.item_pos()
        l3 = self._barbarian_l2.item_pos()

        # print(kingpos[0], kingpos[1], pos[1], pos[0])
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

        self._screen.place_object(self._hut5)
        self._screen.place_object(self._cannon1)
        self._screen.place_object(self._cannon2)

        if(self._kingval == 1):
            self._screen.place_object(self._king)

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

    # def king_val(self):
    #     self._kingattack = 1

    def result(self):
        
        if(self._town._health_val<=0 and self._hut1._health_val<=0 and self._hut2._health_val<=0 and self._hut3._health_val<=0 and self._hut4._health_val<=0 and self._hut5._health_val<=0):
            self._screen.game_won()
            
        elif(self._king._health_val<=0   
            #  and self._barbarian_k._health_val<=0 and self._barbarian_k1._health_val<=0 and self._barbarian_k2._health_val<=0 and self._barbarian_l1._health_val<=0 and self._barbarian_l2._health_val<=0 and self._barbarian_l._health_val<=0 and self._barbarian_p._health_val<=0  and self._barbarian_p1._health_val<=0  and self._barbarian_p2._health_val<=0  ):
        ):
            self._screen.game_lost()
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
            self._kingval = 1
        elif ch == 'd':
            self._king.move(ch)
        elif ch == 'a':
            self._king.move(ch)
        elif ch == 'w':
            self._king.move(ch)
        elif ch == 's':
            self._king.move(ch)
        elif ch == ' ':
            self._kingattack_falg = 1
        elif ch == 'p':
            self._pcounter += 1
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
        itteration  = 0
        path = input()
        print(path)
        self.start()
        f=open("replay/"+str(path)+".txt","r")
        print("harsha :replay/"+str(path)+".txt",end=" ")
        start_time=time.time()
        curr_move=0
        moves=[]
        times=[]
        lines=f.readlines()
        # print(lines[1])
        for line in lines:
            words=line.split(" ")
            if(len(words)==3):
                moves.append(" ")
                x=words[2].rstrip("\n")
                times.append(x)
            else:
                
                # print(words[0],words[1],end=" ")
                y=words[1].rstrip("\n")
                # print(words[0],y,"\n",end=" ")
                moves.append(words[0])
                times.append(y) 
        # for i in range(10):
        #     # print("  ",itteration ,i,moves[i],times[i])
        ff = len(moves)
        print(len(moves),int(times[ff-1]))
        while True:
            self._screen.clean()
            self._screen.reset_screen()
            # print("  ",itteration ,curr_move,moves[curr_move],times[curr_move])
            # if(itteration > int(times[ff-1])):
            #     self.result()
            #     sys.exit()
            if(itteration <= int(times[ff-1])):
                if(itteration == int(times[curr_move])):
                    time.sleep(0.1)
                    # curr_move+=1     
                    # print("coming")
                    ch = moves[curr_move]      
                    if(ch == 'q'):
                        sys.exit()
                    elif(ch == 'k'):
                        self._kingval = 1
                    elif ch == 'd':
                        self._king.move(ch)
                    elif ch == 'a':
                        self._king.move(ch)
                    elif ch == 'w':
                        self._king.move(ch)
                    elif ch == 's':
                        self._king.move(ch)
                    elif ch == ' ':
                        self._kingattack_falg = 1
                    elif ch == 'p':
                        self._pcounter += 1
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
                
                    curr_move+=1           
            self.king_attack()
            self.cannon_attack()
            self.placing()
            self.result()

            self._screen.render_screen()
            itteration+=1

game = Game()
game.run()
