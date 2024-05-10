import pygame

class SpatialHash():
    def __init__(self, window, cellSize):
        self.window = window
        self.cellSize = cellSize
        self.content = {}

    def _hash(self, point):
        return int(point[0]/self.cellSize), int(point[1]/self.cellSize)

    def insert(self, boid):
        minHash, maxHash = self._hash(boid.rect.topleft), self._hash(boid.rect.bottomright)
        for i in range(minHash[0], maxHash[0]+1):
            for j in range(minHash[1], maxHash[1]+1):
                self.content.setdefault((i, j), []).append(boid)

    def getCollisions(self, boid):
        searchArea = boid.vRect
        foundContent = []
        minHash, maxHash = self._hash(searchArea.topleft), self._hash(searchArea.bottomright)
        for i in range(minHash[0], maxHash[0]+1):
            for j in range(minHash[1], maxHash[1]+1):
                if self.content.get((i, j)) is not None:
                    foundContent.append(self.content.get((i,j)))
        return [x for content in foundContent for x in content]
    
    def updateObject(self, boid):
        #change the self.contents dict to use the boidID as a key and a tuple of (boid, hash) for the value
        #then update the boid by usage of the boidID. 
        pass
    
    def draw(self):
        pass
        #cell = pygame.Rect()
        #for item in self.content:
            
        #pygame.draw.rect(self.window, "white", cell, 1)
        
