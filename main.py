from random import uniform
import pygame_widgets
import pygame
from UI import UI
from boid import Boid, WIDTH, HEIGHT
from helpers import mouseInBound
from spatialHash import SpatialHash

# Ideas: implement vision cone instead of the vision being a square.
# Ideas: Add toggle for grouping of boids.

# Disables constant should be UPPER_CASE message
# pylint: disable=C0103

MARGIN = 20
CAPACITY = 8
EDGE_TURN_FACTOR = 0.6
flock = []
spawn = False
running = True
visibleUI = True
avoidEdges = True
buttonClick = False

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
uiWindow = UI(window, WIDTH, HEIGHT)
spatialHash = SpatialHash(window, 16)

while running:
    # wipe away anything from last frame
    window.fill((15, 15, 15))

    sep = uiWindow.sliderSep.getValue()
    align = uiWindow.sliderAlign.getValue()
    coh = uiWindow.sliderCoh.getValue()
    vRad = uiWindow.sliderRad.getValue()
    boidCount = uiWindow.sliderBoidCount.getValue()
    dragCoeff = uiWindow.sliderDrag.getValue()
    behaviourValues = {"separation": sep, "alignment": align, "cohesion": coh, "drag": dragCoeff}
    avoidEdges = uiWindow.edgesToggle.getValue()
    debugVisible = uiWindow.debugToggle.getValue()

    # Poll for events.
    # Press the space bar to hide the UI
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                visibleUI = not visibleUI
        if event.type == pygame.MOUSEBUTTONDOWN:
            spawn = True
        if event.type == pygame.MOUSEBUTTONUP:
            spawn = False
        if spawn:
            if visibleUI:
                pos = pygame.mouse.get_pos()
                if mouseInBound(uiWindow.rect, pos):
                    boid = Boid(pos[0], pos[1], len(flock) + 1)
                    flock.append(boid)
                    #quadTree.insert(boid)
                    uiWindow.sliderBoidCount.setValue(boidCount + 1)
            else:
                pos = pygame.mouse.get_pos()
                boid = Boid(pos[0], pos[1], len(flock) + 1)
                flock.append(boid)
                #quadTree.insert(boid)
                uiWindow.sliderBoidCount.setValue(boidCount + 1)

    if boidCount > len(flock):
        while boidCount > len(flock):
            boid = Boid(uniform(0, WIDTH), uniform(0, HEIGHT), len(flock) + 1)
            flock.append(boid)
            spatialHash.insert(boid)
            
    elif boidCount < len(flock):
        while boidCount < len(flock):
            flock.pop()

    #quadTree = QuadTree(window.get_rect(), CAPACITY)
    #for boid in flock:
        #quadTree.insert(boid)
    #spatialHash = SpatialHash(window, 16)
    #for boid in flock:
    #    spatialHash.insert(boid)
    for boid in flock:
        neighbours = spatialHash.getCollisions(boid)
        #neighbours = quadTree.findInRect(boid.vRect)
        boid.behaviour(neighbours, behaviourValues)
        boid.edges(avoidEdges, MARGIN, EDGE_TURN_FACTOR)
        boid.update(dragCoeff)
        print(id(boid))
        spatialHash.updateBoid(boid)
        boid.draw(window)

    uiWindow.setFps(str(int(clock.get_fps())))
    uiWindow.draw(window, visibleUI, debugVisible, flock)
    pygame_widgets.update(events)
    pygame.display.update()
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
