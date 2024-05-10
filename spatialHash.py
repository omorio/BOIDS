import pygame

class SpatialHash():
    def __init__(self, window, cellSize):
        self.window = window
        self.cellSize = cellSize
        self.content = {}

    def _hash(self, point):
        return int(point.x/self.cellSize), int(point.y/self.cellSize)

    def insert(self, boid):
        minHash, maxHash = self._hash(boid.rect.topleft), self._hash(boid.rect.bottomright)
        for i in range(minHash[0], maxHash[0]+1):
            for j in range(minHash[1], maxHash[1]+1):
                self.content.setdefault((i, j), []).append(boid)

    def getContent(self, searchArea):
        foundContent = []
        minHash, maxHash = self._hash(searchArea.topleft), self._hash(searchArea.bottomright)
        for i in range(minHash[0], maxHash[0]+1):
            for j in range(minHash[1], maxHash[1]+1):
                foundContent.append(self.content.get((i, j)))
        return foundContent
    
    def draw(self):
        pass
        #cell = pygame.Rect()
        #for item in self.content:
            
        #pygame.draw.rect(self.window, "white", cell, 1)
        
