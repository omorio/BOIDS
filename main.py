from random import uniform
import pygame_widgets
import pygame
from UI import UI
from boid import Boid, WIDTH, HEIGHT
from helpers import mouseInBound
from pointQuadTree2 import QuadTree

# TODO: replace blob with traingele and rotate triangle around pivot
# TODO: implement vision cone instead of the vision being a square.
# TODO: Add toggle for grouping of boids.

buttonClick = False
pygame.init()
CAPACITY = 8
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
avoidEdges = True
visibleUI = True
turnFactor = 0.6
margin = 20
flock = []


quadTree = QuadTree(
    window.get_rect(), CAPACITY
)  # put boids in quadTree for easy lookup.

# for i in range(2):
# chaserFlock.append(ChaserBoid(uniform(WIDTH/4, 3*WIDTH/4), uniform(HEIGHT/4, 3*HEIGHT/4)))
spawn = False
uiWindow = UI(window, WIDTH, HEIGHT)
while running:
    # fill the screen with a color to wipe away anything from last frame
    # window.fill((25,25,25))
    window.fill((15, 15, 15))

    # quadTree = QuadTree(flock, window, QTDepth, window.get_rect(), drawTree) # put boids in quadTree for easy lookup.
    # quadTree = QuadTree(flock, window, window.get_rect(), True, capacity, QTDepth) # put boids in quadTree for easy lookup.

    sep = uiWindow.sliderSep.getValue()
    align = uiWindow.sliderAlign.getValue()
    coh = uiWindow.sliderCoh.getValue()
    vRad = uiWindow.sliderRad.getValue()
    boidCount = uiWindow.sliderBoidCount.getValue()
    dragCoeff = uiWindow.sliderDrag.getValue()

    avoidEdges = uiWindow.edgesToggle.getValue()
    debugVisible = uiWindow.debugToggle.getValue()

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_u:
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
                    quadTree.insert(boid)
                    uiWindow.sliderBoidCount.setValue(boidCount + 1)
            else:
                pos = pygame.mouse.get_pos()
                boid = Boid(pos[0], pos[1], len(flock) + 1)
                flock.append(boid)
                quadTree.insert(boid)
                uiWindow.sliderBoidCount.setValue(boidCount + 1)


    if boidCount == len(flock):
        pass
    elif boidCount > len(flock):
        while boidCount > len(flock):
            flock.append(Boid(uniform(0, WIDTH), uniform(0, HEIGHT), len(flock) + 1))
    elif boidCount < len(flock):
        while boidCount < len(flock):
            flock.pop()

    quadTree = QuadTree(window.get_rect(), CAPACITY)
    for boid in flock:
        quadTree.insert(boid)
    for boid in flock:
        boid.values = {"separation": sep, "alignment": align, "cohesion": coh}
        boid.behaviour(quadTree)
        boid.edges(avoidEdges, margin, turnFactor)
        boid.update(dragCoeff)
        boid.draw(window)

    uiWindow.draw(window, visibleUI, debugVisible, quadTree, flock)
    pygame_widgets.update(events)
    pygame.display.update()
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
