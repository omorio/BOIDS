from pointQuadTree2 import QuadTree
from random import uniform
from chaserBoid import *
from boid import *
from UI import *
import pygame


buttonClick = False


pygame.init()
capacity = 8
window = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
avoidEdges = True
visibleUI = True
turnFactor = 0.6
margin = 20
flock = []

# TODO: implement vision cone instead of the vision being a square.
# TODO: Add toggle for grouping of boids.

quadTree = QuadTree(
    window.get_rect(), capacity
)  # put boids in quadTree for easy lookup.

for i in range(1000):
    boid = Boid(uniform(width / 8, 7 * width / 8), uniform(height / 8, 7 * height / 8), i)
    flock.append(boid)
    quadTree.insert(boid)

# for i in range(2):
# chaserFlock.append(ChaserBoid(uniform(width/4, 3*width/4), uniform(height/4, 3*height/4)))
spawn = False
uiWindow = UI(window, width, height)
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
    visibleDebug = uiWindow.debugToggle.getValue()

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
            flock.append(Boid(uniform(0, width), uniform(0, height), len(flock) + 1))
    elif boidCount < len(flock):
        while boidCount < len(flock):
            flock.pop()

    quadTree = QuadTree(window.get_rect(), capacity)
    for boid in flock:
        quadTree.insert(boid)
    for boid in flock:
        boid.behaviour(quadTree)
        boid.edges(avoidEdges, margin, turnFactor)
        boid.update(dragCoeff)
        boid.draw(window, 5, 40)
        boid.values = {"separation": sep, "alignment": align, "cohesion": coh}

    if visibleDebug:
        quadTree.draw(window)
        if len(flock) != 0:
            pygame.draw.rect(window, "white", flock[-1].rect, 2)
            pygame.draw.rect(window, "white", flock[-1].vRect, 2)

    pygame.font.init()
    font = pygame.font.SysFont(None, 24)

    fpsString = str(int(clock.get_fps()))
    fps = font.render(fpsString, True, (255, 255, 255))

    boidCountStr = str(len(flock))
    boidCount = font.render(boidCountStr, True, (255, 255, 255))

    window.blit(fps, (window.get_width() - 50, 50))
    window.blit(boidCount, (window.get_width() - 100, 50))

    uiWindow.draw(window, visibleUI, visibleDebug, margin)
    pygame_widgets.update(events)
    pygame.display.update()
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
