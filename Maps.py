import pygame, sys
import numpy as np
from pygame.locals import *
import time
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
    for i in range(40):
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
    pygame.font.init()
    return pygame.display.set_mode((MAPWIDTH*TILESIZE+200,MAPHEIGHT*TILESIZE))

def uiRefresh(tilemap, data, DISPLAYSURF):
    #get all the user events
    button = pygame.Rect(640, 10, 80, 40)
    eraser = pygame.Rect(640,80,300,300)
    myfont = pygame.font.SysFont('Arial', 20)
    flag = False
    for event in pygame.event.get():
        #if the user wants to quit
        if event.type == QUIT:
            #and the game and close the window
            pygame.quit()
            sys.exit()
            
        
        if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position

                # checks if mouse position is over the button

                if button.collidepoint(mouse_pos):
                    #Shows best solution found so far
                    tilemap = data[0].tilemap
                    flag = True

    #loop through each row
    for row in range(MAPHEIGHT):
        #loop through each column in the row
        for column in range(MAPWIDTH):
            #draw the resource at that position in the tilemap, using the correct colour
            pygame.draw.rect(DISPLAYSURF, colourMap[tilemap[row][column]], (column*TILESIZE,row*TILESIZE,TILESIZE,TILESIZE))

    #Drawing elements
    pygame.draw.rect(DISPLAYSURF, [200, 200, 200], button)
    textsurface1 = myfont.render('View Best', False, (0, 0, 0))
    highString = "Highest Fitness: " + str(data[1])
    currString = "Current Fitness: " + str(data[2])
    pygame.draw.rect(DISPLAYSURF, [0,0,0], eraser)
    textsurface2 = myfont.render(highString,False,(255,255,255))
    textsurface3 = myfont.render(currString,False,(255,255,255))
    DISPLAYSURF.blit(textsurface1,(640,10))
    DISPLAYSURF.blit(textsurface2,(640,80))
    DISPLAYSURF.blit(textsurface3,(640,120))
    
    #update the display
    pygame.display.update()
    if flag == True:
        time.sleep(10)