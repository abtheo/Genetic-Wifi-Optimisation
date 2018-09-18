import Maps
import numpy as np

#CONSTANT DECLARATIONS
SPOTNUM = 20

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
               
        
    #Draw self onto map
    def draw(self, tilemap):
        #Iterates through surrounding map area
        for i in range(self.x_pos - self.spotType, self.x_pos + self.spotType+1):
            for j in range(self.y_pos - self.spotType, self.y_pos + self.spotType+1):
                
                blockedFlag = False
                try:
                    #Ternary operator to determine loop direction
                    direction = 1 if (i < self.x_pos) else -1
                    #Draw imaginary line to origin and check for walls
                    for xBlocking in range(i,self.x_pos, direction):
                        if tilemap[xBlocking, j] == WALL:
                            blockedFlag = True
                     
                    direction = 1 if (j < self.y_pos) else -1
                    for yBlocking in range(j,self.y_pos, direction):
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

#Class comprising the population
class iMap:

    def __init__(self,tilemap,spotList=None):
        if spotList == None:
            self.spotList = self.generateSpots(SPOTNUM)
        else:
            self.spotList = spotList
        self.tilemap = np.copy(tilemap)
        self.fitness = 0
            
    #Returns list of newly generated spots
    def generateSpots(self,n):
        newSpotList = list()
        for i in range(n):
            newSpot = Spot()
            newSpotList.append(newSpot)
        return newSpotList

    #Draws list of spots onto map
    def drawSpots(self):
        #Preserves original map
        for item in self.spotList:
            self.tilemap = item.draw(self.tilemap)
    
    #Evaluates fitness of the iMap
    #Based on allele fitness and overall map coverage
    def mapFitness(self):
        #Amount of open space in original map
        tilemapArea = (self.tilemap == NONE).sum()
        #Draws Wifi spots onto map
        self.drawSpots()
        #Amount of open space after spots drawn
        spotMapArea = (self.tilemap == NONE).sum()
        
        #Gets overall coverage for fitness calculation
        #Equates to percentage of free space now covered by signal
        #signalFitness = 100 - (spotMapArea / tilemapArea * 100)
        signalFitness = tilemapArea - spotMapArea
        #Gets average fitness of each allele
        alleleFitness = 0
        for spot in self.spotList:
            alleleFitness = (alleleFitness + spot.getFitness(self.tilemap))
            
        self.fitness = signalFitness + alleleFitness*1.5
    

#Generates N random population of spotMaps
#Also gets fitness of each map
def generatePopulation(N,tilemap):
    population = list()
    for i in range(N):
        newiMap = iMap(tilemap)
        newiMap.mapFitness()
        population.append(newiMap)
    return population

def pickParents(population,N):
    population.sort(key=lambda x: x.fitness, reverse=True)
    #Only selects best parents
    parents = list()
    for i in range(N):
        parents.append(population[i])
    return parents

#Applies random genetic variation to an individual
def mutate(child):
    #Chance of each mutation
    moveRate = 0.1
    typeRate = 0.01
    
    #Random choices
    mutation = np.random.rand()
    randIndex = np.random.randint(0,len(child.spotList))
    #Moves spot randomly
    if mutation < moveRate:
        #Boundary detection
        child.spotList[randIndex].x_pos = np.random.randint(2,MAPWIDTH-2)
        child.spotList[randIndex].y_pos = np.random.randint(2,MAPHEIGHT-2)
    
    #Changes type of one spot randomly
    if mutation < typeRate:
        child.spotList[randIndex].spotType = np.random.randint(1,4)
        
    return child

#Exchanges genetic information between parents
def crossover(population):
    childSpotList=list()
    #Selects parents and sorts by fitness
    parentNum = 10
    parents = pickParents(population,parentNum)
    
    for p in parents:
        p.spotList.sort(key=lambda x: x.getFitness(p.tilemap), reverse=True)
    index = 0    
    #Exchanges genetic info
    while len(childSpotList) < SPOTNUM:
            
        #Random parent choice
        parentChoice = np.random.randint(0,parentNum)
        for i,p in enumerate(parents):
            if parentChoice == i:
                bestFit = p.spotList[index]
                
        #Exclusivity
        exclusiveFlag = True
        for children in childSpotList:
            if bestFit.x_pos == children.x_pos and bestFit.y_pos == children.y_pos:
                exclusiveFlag = False
        if exclusiveFlag:
            childSpotList.append(bestFit)
        else:
            bestFit.x_pos = np.random.randint(2,MAPWIDTH-2)
            bestFit.y_pos = np.random.randint(2,MAPHEIGHT-2)

        index = (index+1) % SPOTNUM
        
    return childSpotList

#Produces new population of evolved iMaps
def reproduce(population,tilemap):
    newPopulation = list()
    for i in range(SPOTNUM):
        #Swaps genetic information from each parent AKA Crossover
        childSpotList = crossover(population)
        #Spawn a new child
        child = iMap(tilemap,childSpotList)
        #Apply random genetic variation
        mutate(child)
        #Evaluate fitness of mutant child
        child.mapFitness()
        #Add mutant child to new population
        newPopulation.append(child)
        
    return newPopulation

#Initialisations
DISPLAYSURF = Maps.uiInit()
#Generates new random map for algorithm to run inside    
tilemap = Maps.createMap() 
population = generatePopulation(50,tilemap)
highscore = 0
generation = 0
#Genetic Algorithm runs, displays every 10 generations
while True:
    for i in range(10):
        population = reproduce(population,tilemap)
        #Gets best child for display
        bestFitness = 0
        for x,imap in enumerate(population):
            if imap.fitness > bestFitness:
                bestIndex = x
                bestFitness = imap.fitness
  
        if bestFitness > highscore:
            highscore = bestFitness
            bestIndividual = population[bestIndex]
            print("New highscore! Fitness = ", highscore, ", Generation = ",generation)
        
        data = [ bestIndividual, highscore, bestFitness, generation]
        
        Maps.uiRefresh(population[bestIndex].tilemap, data, DISPLAYSURF)
        generation+=1
        
