import pygame
from boid import *
from pointQuadTree2 import QuadTree

buttonClick = False
from UI import *
from random import uniform
from chaserBoid import *


pygame.init()
capacity = 16
width = 2560
height = 1440
window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
avoidEdges = True
visibleUI = False
turnFactor = 0.6
margin = 20
flock = []
#TODO: Add toggle for grouping of boids.

quadTree = QuadTree(window.get_rect(), capacity) # put boids in quadTree for easy lookup.
for i in range(1000):
    boid = Boid(uniform(width / 8, 7 * width / 8), uniform(height / 8, 7 * height / 8))
    flock.append(boid)
    quadTree.insert(boid)

# for i in range(2):
# chaserFlock.append(ChaserBoid(uniform(width/4, 3*width/4), uniform(height/4, 3*height/4)))

uiWindow = UI(window, width, height)
while running:
    # poll for events   
    # pygame.QUIT event means the user clicked X to close your window
    spawn = False
    pos = (0, 0)
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
            pos = pygame.mouse.get_pos()
            if visibleUI:
                if mouseInBound(uiWindow.rect, pos):
                    boid = Boid(pos[0], pos[1])
                    flock.append(boid)
                    quadTree.insert(boid)
                    
            else:
                boid = Boid(pos[0], pos[1])
                flock.append(boid)
                quadTree.insert(boid)

    # fill the screen with a color to wipe away anything from last frame
    # window.fill((25,25,25))
    window.fill((15, 15, 15))

    #quadTree = QuadTree(flock, window, QTDepth, window.get_rect(), drawTree) # put boids in quadTree for easy lookup.
    #quadTree = QuadTree(flock, window, window.get_rect(), True, capacity, QTDepth) # put boids in quadTree for easy lookup.

    sep = uiWindow.sliderSep.getValue()
    align = uiWindow.sliderAlign.getValue()
    coh = uiWindow.sliderCoh.getValue()
    vRad = uiWindow.sliderRad.getValue()

    avoidEdges = uiWindow.edgesToggle.getValue()
    visibleDebug = uiWindow.debugToggle.getValue()

    #chaserSep = uiWindow.chaserSliderSep.getValue()
    #chaserAlign = uiWindow.chaserSliderAlign.getValue()
    #chaserCoh = uiWindow.chaserSliderCoh.getValue()
    #chaserRad = uiWindow.chaserSliderRad.getValue()

    #if uiWindow.delChaserButton.clicked:
    #    chaserFlock.clear()
    
    quadTree = QuadTree(window.get_rect(), capacity)
    for boid in flock:
        quadTree.insert(boid)
    for boid in flock:
        
        #quadTree.insert(boid)
        #boid.vRadius = vRad/2
        boid.behaviour(quadTree)
        boid.edges(width, height, avoidEdges, margin, turnFactor)
        boid.update()
        boid.draw(window, 5, 40)
        boid.values = {"separation": sep, "alignment": align, "cohesion": coh}

    if visibleDebug:
        quadTree.draw(window)
        pygame.draw.rect(window, "white", flock[-1].rect, 2)
        pygame.draw.rect(window, "white", flock[-1].vRect, 2)
        pygame.font.init()
        font = pygame.font.SysFont(None, 24)
        fpsString = str(int(clock.get_fps()))
        fps = font.render(fpsString, True, (255,255,255))
        window.blit(fps, (window.get_width()-50, 50))



    uiWindow.draw(window, visibleUI, visibleDebug, margin)
    pygame_widgets.update(events)
    pygame.display.update()
    pygame.display.flip()

    #print(clock.get_fps())

    clock.tick(60)  # limits FPS to 60

pygame.quit()
