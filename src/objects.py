from wsgiref.handlers import read_environ
from matplotlib.pyplot import cla
import numpy as np
import time
from color import *
import os


class Item:
    def __init__(self, pos, size, height, width, maxsize,health_val,damage):
        self._pos = np.array(pos)
        self._size = np.array(size)
        self._height = height
        self._width = width
        self._maxsize = np.array(maxsize)
        self._structure = np.array([[]])
        self._health = np.array([[]])
        self._health_val = health_val
        self._damage = damage

    def get_dimension(self):
        return [self._pos, self._size, self._height, self._width, self._maxsize,self._health_val,self._damage]

    def get_structure(self):
        return self._structure
    def get_health(self):
        return self._health

class Town(Item):
    def __init__(self, pos, size, height, width, maxsize,health_val,damage):
        super().__init__(pos, size, height, width, maxsize,health_val,damage)
        # self._structure = np.array([[bg.yellow+' '+reset for j in range(self._size[1])]for i in range(size[0])],dtype='object')

        # var = []
        # for i in range(size[0]):
        #     temp=[]
        #     for j in range(self._size[1]):
        #         temp.append(bg.yellow+' '+reset)
        #     var.append(temp)

        # self._structure =np.array(var,dtype='object')

        
        self._structure = np.zeros(
            (self._size[0], self._size[1]), dtype='object')
        for i in range(size[0]):
            for j in range(size[1]):
                self._structure[i][j] = bg.blue +' '+reset
                if(j == 3 and i != 0 and i != size[0]-1):
                    self._structure[i][j] = bg.black+'  '+reset+bold
                    self._structure[i][j] = 'T'+reset+bold
        
        self._health = np.zeros(
            (int(2), self._size[1]), dtype='object')
        for i in range(2):
            for j in range(size[1]):
                if(self._health_val>50):
                    self._health[i][j] = bg.green+' '+reset
                elif (self._health_val>20):
                    self._health[i][j] = bg.yellow+' '+reset
                else:
                    self._health[i][j] =bg.red+' '+reset
    def update_health(self,damage):
        self._health_val = self._health_val - damage               
               
    def get_health(self):
        return self._health_val

class King(Item):
    def __init__(self, pos, size, height, width, maxsize,health_val,damage):
        super().__init__(pos, size, height, width, maxsize,health_val,damage)
        self._mov = 1
  
        # speed = 1
            
        self._structure = np.zeros(
            (self._size[0], self._size[1]), dtype='object')
        for i in range(self._size[0]):
            for j in range(self._size[1]):
                self._structure[i][j] = bg.red+' '+reset
                if(j == 2 and i != 0 and i != size[0]-1):
                    self._structure[i][j] = bg.black+'  '+reset
                    self._structure[i][j] = 'K'+reset+bold
        self._health = np.zeros(
            (int(2), self._size[1]), dtype='object')
        for i in range(2):
            for j in range(size[1]):
                if(self._health_val>50):
                    self._health[i][j] = bg.green+' '+reset
                elif (self._health_val>20):
                    self._health[i][j] = bg.yellow+' '+reset
                else:
                    self._health[i][j] =bg.red+' '+reset
                    
    def item_pos(self):
        return self._pos
    def range_spell(self):
        self._damage = 2 * self._damage
        self._mov = 2 * self._mov
    def move(self, ch):
        if(ch == 'd'):
            self._pos[0] = self._pos[0]+ self._mov
            if(self._pos[0]+self._size[0] >= self._maxsize[0]-1):
                self._pos[0] = self._maxsize[0] - self._size[0] - 3
        elif(ch == 'a'):
            self._pos[0] = self._pos[0]-self._mov
            if(self._pos[0] <= 4):
                self._pos[0] = 4
        elif(ch == 'w'):
            self._pos[1] = self._pos[1]-self._mov
            if(self._pos[1] <= 4):
                self._pos[1] = 1
        elif(ch == 's'):
            if(self._pos[1]+self._size[1] >= self._maxsize[1]-1):
                self._pos[1] = self._maxsize[1] - self._size[1]-2
            else:
                self._pos[1] = self._pos[1]+self._mov
                    
                
    def update_health(self,damage):
        if(self._health_val>0):
         self._health_val = self._health_val - damage
        
    def heal_spell(self):
        if(int(1.5*self._health_val) > 100 ):
            self._health_val = 100
        else :
            self._health_val = int((1.5)*self._health_val)

class Queen(Item):
    def __init__(self, pos, size, height, width, maxsize,health_val,damage):
        super().__init__(pos, size, height, width, maxsize,health_val,damage)
        self._mov = 1
  
        # speed = 1
            
        self._structure = np.zeros(
            (self._size[0], self._size[1]), dtype='object')
        for i in range(self._size[0]):
            for j in range(self._size[1]):
                self._structure[i][j] = bg.green+' '+reset
                if(j == 2 and i != 0 and i != size[0]-1):
                    self._structure[i][j] = bg.black+'  '+reset
                    self._structure[i][j] = 'K'+reset+bold
        self._health = np.zeros(
            (int(2), self._size[1]), dtype='object')
        for i in range(2):
            for j in range(size[1]):
                if(self._health_val>50):
                    self._health[i][j] = bg.green+' '+reset
                elif (self._health_val>20):
                    self._health[i][j] = bg.yellow+' '+reset
                else:
                    self._health[i][j] =bg.red+' '+reset
                    
    def item_pos(self):
        return self._pos
    def range_spell(self):
        self._damage = 2 * self._damage
        self._mov = 2 * self._mov
    def move(self, ch):
        if(ch == 'd'):
            self._pos[0] = self._pos[0]+ self._mov
            if(self._pos[0]+self._size[0] >= self._maxsize[0]-1):
                self._pos[0] = self._maxsize[0] - self._size[0] - 3
        elif(ch == 'a'):
            self._pos[0] = self._pos[0]-self._mov
            if(self._pos[0] <= 4):
                self._pos[0] = 4
        elif(ch == 'w'):
            self._pos[1] = self._pos[1]-self._mov
            if(self._pos[1] <= 4):
                self._pos[1] = 1
        elif(ch == 's'):
            if(self._pos[1]+self._size[1] >= self._maxsize[1]-1):
                self._pos[1] = self._maxsize[1] - self._size[1]-2
            else:
                self._pos[1] = self._pos[1]+self._mov
                    
                
    def update_health(self,damage):
        if(self._health_val>0):
         self._health_val = self._health_val - damage
        
    def heal_spell(self):
        if(int(1.5*self._health_val) > 100 ):
            self._health_val = 100
        else :
            self._health_val = int((1.5)*self._health_val)

class Hut(Item):
    def __init__(self, pos, size, height, width, maxsize,health_val,damage):
        super().__init__(pos, size, height, width, maxsize,health_val,damage)

        self._structure = np.zeros(
            (self._size[0], self._size[1]), dtype='object')
        for i in range(self._size[0]):
            for j in range(self._size[1]):
                self._structure[i][j] = bg.cyan+' '+reset
                if(j == 2 and i != 0 and i != size[0]-1):
                    self._structure[i][j] = bg.black+'  '+reset
                    self._structure[i][j] = 'H'+reset+bold
        self._health = np.zeros(
            (int(2), self._size[1]), dtype='object')
        for i in range(1):
            for j in range(size[1]):
                if(self._health_val>50):
                    self._health[i][j] = bg.green+' '+reset
                elif (self._health_val>20):
                    self._health[i][j] = bg.yellow+' '+reset
                else:
                    self._health[i][j] =bg.red+' '+reset
    
    def update_health(self,damage):
        self._health_val = self._health_val - damage
    def hut_health(self):
        return self._health_val
    
    
        
    
class Cannon(Item):
    def __init__(self, pos, size, height, width, maxsize,health_val,damage):
        super().__init__(pos, size, height, width, maxsize,health_val,damage)

        self._structure = np.zeros(
            (self._size[0], self._size[1]), dtype='object')
        for i in range(self._size[0]):
            for j in range(self._size[1]):
                self._structure[i][j] = bg.lightgrey+' '+reset
                if(j == 2 and i != 0 and i != size[0]-1):
                    self._structure[i][j] = bg.black+'  '+reset
                    self._structure[i][j] = 'C'+reset+bold
        self._health = np.zeros(
            (int(2), self._size[1]), dtype='object')
        for i in range(2):
            for j in range(size[1]):
                if(self._health_val>50):
                    self._health[i][j] = bg.green+' '+reset
                elif (self._health_val>20):
                    self._health[i][j] = bg.yellow+' '+reset
                else:
                    self._health[i][j] =bg.red+' '+reset
                    
    def update_health(self,damage):
        self._health_val = self._health_val - damage
    def item_pos(self):
        return self._pos 
    def can_health(self):
        return self._health_val 
    
class WizardTower(Item):
    def __init__(self, pos, size, height, width, maxsize,health_val,damage):
        super().__init__(pos, size, height, width, maxsize,health_val,damage)

        self._structure = np.zeros(
            (self._size[0], self._size[1]), dtype='object')
        for i in range(self._size[0]):
            for j in range(self._size[1]):
                self._structure[i][j] = bg.cyan+' '+reset
                # if(j == 2 and i != 0 and i != size[0]-1):
                #     self._structure[i][j] = bg.black+'  '+reset
                #     self._structure[i][j] = 'C'+reset+bold
        self._health = np.zeros(
            (int(2), self._size[1]), dtype='object')
        for i in range(2):
            for j in range(size[1]):
                if(self._health_val>50):
                    self._health[i][j] = bg.green+' '+reset
                elif (self._health_val>20):
                    self._health[i][j] = bg.yellow+' '+reset
                else:
                    self._health[i][j] =bg.red+' '+reset
                    
    def update_health(self,damage):
        self._health_val = self._health_val - damage
    def item_pos(self):
        return self._pos 
    def can_health(self):
        return self._health_val 
    

        
class Wall(Item):
    def __init__(self, pos, size, height, width, maxsize,health_val,damage):
        super().__init__(pos, size, height, width, maxsize,health_val,damage)
        
        
        self._structure = np.zeros(
            (self._size[0], self._size[1]), dtype='object')
        for i in range(self._size[0]):
            for j in range(self._size[1]):
                self._structure[i][j] = bg.purple+' '+reset
                if(j == 2 and i != 0 and i != size[0]-1):
                    self._structure[i][j] = bg.black+'  '+reset
                    self._structure[i][j] = 'W'+reset+bold
        self._health = np.zeros(
            (int(2), self._size[1]), dtype='object')
        for i in range(2):
            for j in range(size[1]):
                if(self._health_val>50):
                    self._health[i][j] = bg.green+' '+reset
                elif (self._health_val>20):
                    self._health[i][j] = bg.yellow+' '+reset
                else:
                    self._health[i][j] =bg.red+' '+reset
                    
    def update_health(self,damage):
        self._health_val = self._health_val - damage
    def wall_health(self):
        return self._health_val
        
class Barbarian(Item):
    
    def __init__(self, pos, size, height, width, maxsize,health_val,damage):
        super().__init__(pos, size, height, width, maxsize,health_val,damage) 
        self._structure = np.zeros(
            (self._size[0], self._size[1]), dtype='object')
        for i in range(self._size[0]):
            for j in range(self._size[1]):
                self._structure[i][j] = bg.purple+' '+reset
                if(j == 2 and i != 0 and i != size[0]-1):
                    self._structure[i][j] = bg.black+'  '+reset
                    self._structure[i][j] = 'B'+reset+bold
        self._health = np.zeros(
            (int(2), self._size[1]), dtype='object')
        for i in range(2):
            for j in range(size[1]):
                if(self._health_val>50):
                    self._health[i][j] = bg.green+' '+reset
                elif (self._health_val>20):
                    self._health[i][j] = bg.yellow+' '+reset
                else:
                    self._health[i][j] =bg.red+' '+reset
           
    def item_pos(self):
        return self._pos               
                
    def update_health(self,damage):
        self._health_val = self._health_val - damage
    
    def range_spell(self):
        self._damage += self._damage
        # self._mov = 2 * self._mov
    def heal_spell(self):
        if(int(1.5*self._health_val) > 100 ):
            self._health_val = 100
        else :
            self._health_val = int((1.5)*self._health_val)
            
            
class Archer(Item):
    
    def __init__(self, pos, size, height, width, maxsize,health_val,damage):
        super().__init__(pos, size, height, width, maxsize,health_val,damage) 
        self._structure = np.zeros(
            (self._size[0], self._size[1]), dtype='object')
        for i in range(self._size[0]):
            for j in range(self._size[1]):
                self._structure[i][j] = bg.blue +' '+reset
        self._health = np.zeros(
            (int(2), self._size[1]), dtype='object')
        for i in range(2):
            for j in range(size[1]):
                if(self._health_val>30):
                    self._health[i][j] = bg.green+' '+reset
                elif (self._health_val>20):
                    self._health[i][j] = bg.yellow+' '+reset
                else:
                    self._health[i][j] =bg.red+' '+reset
           
    def item_pos(self):
        return self._pos               
                
    def update_health(self,damage):
        self._health_val = self._health_val - damage
        
class Balloon(Item):
    
    def __init__(self, pos, size, height, width, maxsize,health_val,damage):
        super().__init__(pos, size, height, width, maxsize,health_val,damage) 
        self._structure = np.zeros(
            (self._size[0], self._size[1]), dtype='object')
        for i in range(self._size[0]):
            for j in range(self._size[1]):
                self._structure[i][j] = bg.cyan +' '+reset
        self._health = np.zeros(
            (int(2), self._size[1]), dtype='object')
        for i in range(2):
            for j in range(size[1]):
                if(self._health_val>30):
                    self._health[i][j] = bg.green+' '+reset
                elif (self._health_val>20):
                    self._health[i][j] = bg.yellow+' '+reset
                else:
                    self._health[i][j] =bg.red+' '+reset
           
    def item_pos(self):
        return self._pos               
                
    def update_health(self,damage):
        self._health_val = self._health_val - damage
    

