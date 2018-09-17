import pygame, sys
import numpy as np
from pygame.locals import *

#constants representing colourMap
BLACK = (0,   0,   0  )
WHITE = (255, 255, 255)
RED = (255, 0,  0  )
GREEN = (0,   255, 0  )
BLUE  = (0,   0,   255)
PURPLE = (140, 0, 190)

#Constants representing map resources
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
TILESIZE  = 10
MAPWIDTH  = 64
MAPHEIGHT = 64

def createMap():
    #Generates new map with border
    tilemap = np.ones( (MAPWIDTH,MAPHEIGHT) )
    tilemap[1:-1,1:-1] = 0
    tilemap = np.multiply(tilemap,5)

    #Generating walls
    for i in range(20):
        coinFlip = np.random.randint(0,2) #X or Y direction
        length = np.random.randint(5,40)
        x_start = np.random.randint(0,MAPWIDTH)
        y_start = np.random.randint(0,MAPHEIGHT)
        
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
    
    return tilemap

#Initialise display    
def uiInit():
    pygame.init()
    return pygame.display.set_mode((MAPWIDTH*TILESIZE,MAPHEIGHT*TILESIZE))

def uiRefresh(tilemap, DISPLAYSURF):
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