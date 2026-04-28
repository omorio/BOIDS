from random import uniform
import pygame_widgets
import pygame
from UI import UI
from boid import Boid, WIDTH, HEIGHT
from helpers import mouseInBound
from pointQuadTree2 import QuadTree

MARGIN = 20
CAPACITY = 8
EDGE_TURN_FACTOR = 0.6


class Simulation:
    def __init__(self):
        self.flock = []
        self.spawn = False
        self.running = True
        self.visibleUI = True
        self.avoidEdges = True

        pygame.init()
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        self.quadTree = QuadTree(self.window.get_rect(), CAPACITY)
        self.uiWindow = UI(self.window, WIDTH, HEIGHT)

    def run(self):
        while self.running:
            self._update()
        pygame.quit()

    def _handle_events(self, events, boidCount):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.visibleUI = not self.visibleUI
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.spawn = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.spawn = False
            if self.spawn:
                pos = pygame.mouse.get_pos()
                if self.visibleUI and not mouseInBound(self.uiWindow.rect, pos, HEIGHT):
                    return
                boid = Boid(pos[0], pos[1], len(self.flock) + 1)
                self.flock.append(boid)
                self.quadTree.insert(boid)
                self.uiWindow.sliderBoidCount.setValue(boidCount + 1)

    def _sync_flock_count(self, boidCount):
        while boidCount > len(self.flock):
            self.flock.append(Boid(uniform(0, WIDTH), uniform(0, HEIGHT), len(self.flock) + 1))
        while boidCount < len(self.flock):
            self.flock.pop()

    def _update(self):
        self.window.fill((15, 15, 15))

        sep = self.uiWindow.sliderSep.getValue()
        align = self.uiWindow.sliderAlign.getValue()
        coh = self.uiWindow.sliderCoh.getValue()
        dragCoeff = self.uiWindow.sliderDrag.getValue()
        boidCount = self.uiWindow.sliderBoidCount.getValue()
        behaviourValues = {"separation": sep, "alignment": align, "cohesion": coh, "drag": dragCoeff}
        self.avoidEdges = self.uiWindow.edgesToggle.getValue()
        debugVisible = self.uiWindow.debugToggle.getValue()

        events = pygame.event.get()
        self._handle_events(events, boidCount)
        self._sync_flock_count(boidCount)

        self.quadTree.clear()
        for boid in self.flock:
            self.quadTree.insert(boid)
        for boid in self.flock:
            boid.behaviour(self.quadTree, behaviourValues)
            boid.edges(self.avoidEdges, MARGIN, EDGE_TURN_FACTOR)
            boid.update(dragCoeff)
            boid.draw(self.window)

        self.uiWindow.setFps(str(int(self.clock.get_fps())))
        self.uiWindow.draw(self.window, self.visibleUI, debugVisible, self.quadTree, self.flock)
        pygame_widgets.update(events)
        pygame.display.update()
        pygame.display.flip()

        self.clock.tick(60)


if __name__ == "__main__":
    Simulation().run()
