import pygame
class QuadTree(object):
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.items = []
        self.split = False

    def divide(self):
    # Calculate the coordinates of the center of the boundary
        cx, cy = self.boundary.centerx, self.boundary.centery

        # Calculate half width and half height for new quadrants
        half_w = self.boundary.width // 2
        half_h = self.boundary.height // 2

        # Define rectangles for each quadrant
        neRect = pygame.Rect(cx, cy - half_h, half_w, half_h)
        self.neQT = QuadTree(neRect, self.capacity)

        nwRect = pygame.Rect(cx - half_w, cy - half_h, half_w, half_h)
        self.nwQT = QuadTree(nwRect, self.capacity)

        seRect = pygame.Rect(cx, cy, half_w, half_h)
        self.seQT = QuadTree(seRect, self.capacity)

        swRect = pygame.Rect(cx - half_w, cy, half_w, half_h)
        self.swQT = QuadTree(swRect, self.capacity)

        self.split = True

    def insert(self, item):
        if (not self.boundary.collidepoint(item.position.x, item.position.y)):
            return False
        if (len(self.items) < self.capacity):
            self.items.append(item)
            return True
        if (not self.split):
            self.divide()
        if (self.neQT.insert(item) or self.nwQT.insert(item) or self.seQT.insert(item) or self.swQT.insert(item)):
            return True
    
    def hit(self, range, found=None):
        if found is None:
            found = []
        if (not range.colliderect(self.boundary)):
            return
        else:
            for boid in self.items:
                if (range.colliderect(boid.rect)): #maybe have to replace .contains with .colliderect
                    found.append(boid)
            if (self.split):
                self.neQT.hit(range, found) 
                self.nwQT.hit(range, found) 
                self.seQT.hit(range, found) 
                self.swQT.hit(range, found) 
        return found

    def draw(self, window, color=(128,128,128)):
        pygame.draw.rect(window, color, self.boundary, 2)
        if(self.split):
            self.nwQT.draw(window, (0,128,0))
            self.neQT.draw(window, (0,0,128))
            self.swQT.draw(window, (128,0,128))
            self.seQT.draw(window, (128,128,0))
        
#comment