import pygame, sys
import numpy as np
import random
from pygame.locals import *

#constants representing colourMap
BLACK = (0,   0,   0  )
WHITE = (255, 255, 255)
RED = (255, 0,  0  )
GREEN = (0,   255, 0  )
BLUE  = (0,   0,   255)
PURPLE = (140, 0, 190)

#constants representing the different resources
NONE  = 0
LOW = 1
MED = 2
HIGH  = 3
SPOT = 4
WALL = 5

#a dictionary linking resources to colourMap
colourMap =   {
                NONE  : WHITE,
                LOW : GREEN,
                MED : BLUE,
                HIGH  : RED,
                SPOT : PURPLE,
                WALL : BLACK
            }

#Dimensions
TILESIZE  = 20
MAPWIDTH  = 40
MAPHEIGHT = 40

#Generates new map with border
tilemap = np.ones( (MAPWIDTH,MAPHEIGHT) )
tilemap[1:-1,1:-1] = 0
tilemap = np.multiply(tilemap,5)

#Generating walls
for i in range(20):
    coinFlip = np.random.randint(0,2) #X or Y direction
    length = np.random.randint(5,15)
    x_start = np.random.randint(0,40)
    y_start = np.random.randint(0,40)
    
    #Draws either vertically or horizontally
    try:
        if coinFlip:
            for i in range(x_start,x_start+length):
                tilemap[i,y_start] = WALL
        else:
            for j in range(y_start,y_start+length):
                tilemap[x_start,j] = WALL
    except IndexError:
        next

#Initialise display
pygame.init()
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE,MAPHEIGHT*TILESIZE))

#Superclass for wifi hotspots
class Spot:
    def __init__(self, x=None, y=None):
        #Handling for optional parameters
        if x and y:
            self.x_pos = x
            self.y_pos = y 
        else:
            self.x_pos = np.random.randint(1,MAPWIDTH-1)
            self.y_pos = np.random.randint(1,MAPHEIGHT-1)
               
        
    def draw(self, tilemap):
        if self.spotType:
            #Iterates through surrounding map area
            for i in range(self.x_pos - self.spotType, self.x_pos + self.spotType+1):
                for j in range(self.y_pos - self.spotType, self.y_pos + self.spotType+1):
                    
                    blockedFlag = False
                    try:
                        #Draw line to origin and check for walls
                        for xBlocking in range(i,self.x_pos):
                            if tilemap[xBlocking, j] == WALL:
                                blockedFlag = True
                                
                        for yBlocking in range(j,self.y_pos):
                            if tilemap[i, yBlocking] == WALL:
                                blockedFlag = True
                         
                        #Collision priorities
                        if tilemap[i,j] < self.spotType:
                            if blockedFlag == False:
                                tilemap[i,j] = self.spotType
                                
                    except IndexError:
                        next
                        
        tilemap[self.x_pos,self.y_pos] = SPOT
                   
                  
class lowSpot(Spot):
    def __init__(self, x=None, y=None):
        Spot.__init__(self, x, y)
        self.spotType = LOW
        #Other vars like energy / price
        
class medSpot(Spot):
    def __init__(self, x=None, y=None):
        Spot.__init__(self, x, y)
        self.spotType = MED
        #Other vars like energy / price
        
class highSpot(Spot):
    def __init__(self, x=None, y=None):
        Spot.__init__(self, x, y)
        self.spotType = HIGH
        #Other vars like energy / price
        
        
#Returns list of newly generated spots
def generateSpots(n):
    newSpotList = list()
    spotChoices = [lowSpot, medSpot, highSpot]
    for i in range(n):
        chosen = random.choice(spotChoices)
        newSpot = chosen()
        newSpotList.append(newSpot)
        
    return newSpotList

#Draws list of spots onto map
def drawSpots(spotList,tilemap):
    for item in spotList:
        item.draw(tilemap)

drawSpots(generateSpots(5),tilemap)

#UI Refresh Loop
while True:
    #get all the user events
    for event in pygame.event.get():
        #if the user wants to quit
        if event.type == QUIT:
            #and the game and close the window
            pygame.quit()
            sys.exit()

    #loop through each row
    for row in range(MAPHEIGHT):
        #loop through each column in the row
        for column in range(MAPWIDTH):
            #draw the resource at that position in the tilemap, using the correct colour
            pygame.draw.rect(DISPLAYSURF, colourMap[tilemap[row][column]], (column*TILESIZE,row*TILESIZE,TILESIZE,TILESIZE))

    #update the display
    pygame.display.update()