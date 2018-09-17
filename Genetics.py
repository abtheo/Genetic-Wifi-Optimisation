import Maps
import numpy as np

#CONSTANT DECLARATIONS
SPOTNUM = 30

#Dimensions
TILESIZE  = 10
MAPWIDTH  = 64
MAPHEIGHT = 64

#Constants representing map resources
NONE  = 0
LOW = 1
MED = 2
HIGH  = 3
SPOT = 4
WALL = 5

#Class for Wifi hotspots
class Spot:
    def __init__(self, x=None, y=None):
        #Handling for optional parameters
        if x and y:
            self.x_pos = x
            self.y_pos = y 
        else:
            self.x_pos = np.random.randint(1,MAPWIDTH-1)
            self.y_pos = np.random.randint(1,MAPHEIGHT-1)
        
        self.spotType = np.random.randint(1,4)
               
        
    def draw(self, tilemap):
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
                    
        #Marks location of the spot itself
        tilemap[self.x_pos,self.y_pos] = SPOT
        #Returns map with spot & signal drawn
        return tilemap
    
    #Fitness function for genetic algorithm
    #NOTE: Must be called AFTER drawn onto map
    def getFitness(self, tilemap):
        signalCounter = 0
        #Iterates through surrounding map area
        for i in range(self.x_pos - self.spotType, self.x_pos + self.spotType+1):
            for j in range(self.y_pos - self.spotType, self.y_pos + self.spotType+1):
                try:
                    if tilemap[i,j] == self.spotType:
                        signalCounter+=1
                except IndexError:
                    next
                    
        signalSizes= {
                LOW : 3*3,
                MED : 5*5,
                HIGH : 7*7}
        
        fitness = signalCounter / signalSizes.get(self.spotType) * 100
        return fitness
                   
        
#Returns list of newly generated spots
def generateSpots(n):
    newSpotList = list()
    for i in range(n):
        newSpot = Spot()
        newSpotList.append(newSpot)
    return newSpotList

#Draws list of spots onto map
def drawSpots(spotList,tilemap):
    #Preserves original map
    localMap = np.copy(tilemap)
    for item in spotList:
        localMap = item.draw(localMap)
    return localMap

#Generates N random population of spotMaps
#Also gets their fitness
def generatePopulation(N,tilemap):
    population = list()
    for i in range(N):
        spotList = generateSpots(SPOTNUM)
        population.append(mapFitness(spotList,tilemap))
    return population
    
#Evaluates percentage of white covered
#So needs a copy of original map (throughout generations)    
def mapFitness(spotList, tilemap):
    #Amount of open space in original map
    tilemapArea = (tilemap == NONE).sum()
    #Draws Wifi spots onto map
    spotMap = drawSpots(spotList,tilemap)
    #Amount of open space after spots drawn
    spotMapArea = (spotMap == NONE).sum()
    
    #Gets overall coverage for fitness calculation
    #Equates to percentage of free space now covered by signal
    signalFitness = 100 - (spotMapArea / tilemapArea * 100)
    
    #Gets average fitness of each allele
    alleleFitness = 0
    for spot in spotList:
        alleleFitness += spot.getFitness(tilemap) / 2
    
    fitness = signalFitness + alleleFitness
    return fitness, spotMap

#Generates new random map for algorithm to run inside    
tilemap = Maps.createMap() 
population = generatePopulation(10,tilemap)
#Maps.uiRefresh(spotMap)