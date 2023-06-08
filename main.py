import pygame
from boid import *
buttonClick = False
from UI import *
from random import uniform
from chaserBoid import *


pygame.init()
window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
flock = []
avoidEdges = True
visibleUI = True
chaserFlock = []
turnFactor = 0.6
margin = 20


for i in range(150):
    flock.append(Boid(uniform(width/4, 3*width/4), uniform(height/4, 3*height/4)))

#for i in range(2):
    #chaserFlock.append(ChaserBoid(uniform(width/4, 3*width/4), uniform(height/4, 3*height/4)))

uiWindow = UI(window, width, height, chaserFlock) 
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    spawn = False
    pos = (0,0)
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
                    spawn = True
            else:
                spawn = True

    # fill the screen with a color to wipe away anything from last frame
    #window.fill((25,25,25))
    window.fill((15,15,15))
    # Spawn a new boid by appending it to the flock array
    sep = uiWindow.sliderSep.getValue()
    align = uiWindow.sliderAlign.getValue()
    coh = uiWindow.sliderCoh.getValue()
    rad = uiWindow.sliderRad.getValue()

    avoidEdges = uiWindow.edgesToggle.getValue()
    visibleDebug = uiWindow.debugToggle.getValue()

    chaserSep = uiWindow.chaserSliderSep.getValue()
    chaserAlign = uiWindow.chaserSliderAlign.getValue()
    chaserCoh = uiWindow.chaserSliderCoh.getValue()
    chaserRad = uiWindow.chaserSliderRad.getValue()

    if uiWindow.delChaserButton.clicked:
        chaserFlock.clear()

    if spawn:
        x = pos[0]
        y = pos[1]
        #flock.pop()
        chaserFlock.append(ChaserBoid(x, y))
    # Draw the boids

    for boid in flock:
        boid.radius = rad
        boid.behaviour(chaserFlock ,flock)
        boid.edges(width, height, avoidEdges, margin, turnFactor)
        boid.update()
        boid.draw(window, 5, 40)
        boid.values = {"separation":sep, "alignment":align, "cohesion":coh}
    
    for chaser in chaserFlock:
        chaser.radius = chaserRad
        chaser.behaviour(chaserFlock, flock)
        chaser.edges(width, height, avoidEdges, margin, turnFactor)
        chaser.draw(window, 5, 40)
        chaser.update()
        chaser.values = {"separation":chaserSep, "alignment":chaserAlign, "cohesion":chaserCoh}



    # flip() the display to put your work on screen

    if visibleDebug:
        pygame.draw.circle(window, "white", (flock[0].position.x, flock[0].position.y), rad, 1)
        pygame.draw.circle(window, "white", (flock[0].position.x, flock[0].position.y), rad/3, 1)
        if chaserFlock:
            pygame.draw.circle(window, "white", (chaserFlock[0].position.x, chaserFlock[0].position.y), chaserRad, 1)
            pygame.draw.circle(window, "white", (chaserFlock[0].position.x, chaserFlock[0].position.y), chaserRad/3, 1)

    uiWindow.draw(window, visibleUI, visibleDebug, margin)
    pygame_widgets.update(events)
    pygame.display.update()
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()