import Maps
import numpy as np

#Maps.uiRefresh()

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

def mapFitness():
    

def spotFitness():
    


#drawSpots(generateSpots(5),tilemap)