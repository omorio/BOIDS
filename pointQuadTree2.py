import pygame
class QuadTree():
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.items = []
        self.split = False
        self.neQT = None
        self.nwQT = None
        self.seQT = None
        self.swQT = None

    def divide(self):
    # Calculate the coordinates of the center of the boundary
        cx, cy = self.boundary.centerx, self.boundary.centery

        # Calculate half width and half height for new quadrants
        halfWidth = self.boundary.width // 2
        halfHeight = self.boundary.height // 2

        # Define rectangles for each quadrant
        neRect = pygame.Rect(cx, cy - halfHeight, halfWidth, halfHeight)
        self.neQT = QuadTree(neRect, self.capacity)

        nwRect = pygame.Rect(cx - halfWidth, cy - halfHeight, halfWidth, halfHeight)
        self.nwQT = QuadTree(nwRect, self.capacity)

        seRect = pygame.Rect(cx, cy, halfWidth, halfHeight)
        self.seQT = QuadTree(seRect, self.capacity)

        swRect = pygame.Rect(cx - halfWidth, cy, halfWidth, halfHeight)
        self.swQT = QuadTree(swRect, self.capacity)

        self.split = True

    def insert(self, item):
        if not self.boundary.collidepoint(item.position.x, item.position.y):
            return False
        if len(self.items) < self.capacity:
            self.items.append(item)
            return True
        if not self.split:
            self.divide()
        if self.neQT.insert(item) or self.nwQT.insert(item) or self.seQT.insert(item) or self.swQT.insert(item):
            return True

    def findInRect(self, rect, found=None):
        if found is None:
            found = []
        if not rect.colliderect(self.boundary):
            return None
        else:
            for boid in self.items:
                if rect.colliderect(boid.rect):
                    found.append(boid)
            if self.split:
                self.neQT.findInRect(rect, found)
                self.nwQT.findInRect(rect, found)
                self.seQT.findInRect(rect, found)
                self.swQT.findInRect(rect, found)
        return found

    def draw(self, window, color=(128,128,128)):
        pygame.draw.rect(window, color, self.boundary, 1)
        if self.split:
            self.nwQT.draw(window, (255,255,255))
            self.neQT.draw(window, (255,255,255))
            self.swQT.draw(window, (255,255,255))
            self.seQT.draw(window, (255,255,255))
