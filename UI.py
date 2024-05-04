import pygame
from pygame_widgets.slider import Slider
from pygame_widgets.toggle import Toggle

initialSep = 2.0
initialAlign = 0.55
initialCoh = 0.25

clock = pygame.time.Clock()

class UI:
    def __init__(self, window, width, height):
        self.width = width
        self.height = height
        self.widgetSpacing = 50
        self.rect = pygame.Rect(8*self.width/10, self.height/10, 6*self.width/8, 8*self.height/10)
        self.rightPadding = 7.5*(self.width - self.rect.x)/10
        self.rectMid = self.rect.x + self.rightPadding/6
        self.UIbackground = pygame.Surface((self.width/5, 8*self.height/10), pygame.SRCALPHA | pygame.FULLSCREEN)
        self.widgetList = []
        self.debugWidgetList = []
#Sliders and text for boids----------------------------------------------------------------------------------
        self.sliderSep = Slider(window, self.rectMid, self.rect.y+self.widgetSpacing, self.rightPadding, 20, 
                                min=0, max=3, step=0.01, initial=initialSep)
        self.sliderAlign = Slider(window, self.rectMid, self.rect.y+self.widgetSpacing*2, self.rightPadding, 20, 
                                  min=0, max=1, step=0.01, initial=initialAlign)
        self.sliderCoh = Slider(window, self.rectMid, self.rect.y + self.widgetSpacing*3, self.rightPadding, 20, 
                                min=0, max=1, step=0.01, initial = initialCoh)
        self.sliderRad = Slider(window, self.rectMid, self.rect.y + self.widgetSpacing*4, self.rightPadding, 20,
                                min=20, max=100, step=2, initial=60)
        self.sliderBoidCount = Slider(window, self.rectMid, self.rect.y + self.widgetSpacing * 5, self.rightPadding, 20, 
                                min=0, max=5000, step=1, initial=1000)
        self.sliderDrag = Slider(window, self.rectMid, self.rect.y + self.widgetSpacing * 6, self.rightPadding, 20, 
                                min=0, max=0.1, step=0.01, initial=0.04)

        self.font = pygame.font.SysFont(None, 24)

        self.sepText = self.font.render('Seperation', True, (255,255,255))
        self.alignText = self.font.render('Alignment', True, (255,255,255))
        self.cohText = self.font.render('Cohesion', True, (255,255,255))
        self.radText = self.font.render('Vision radius', True, (255,255,255))
        self.boidCountText = self.font.render('Boid count', True, (255,255,255))
        self.dragText = self.font.render('Drag', True, (255,255,255))

        self.widgetList.append((self.sepText, (self.rectMid, self.sliderSep._y-20)))
        self.widgetList.append((self.alignText, (self.rectMid, self.sliderAlign._y-20)))
        self.widgetList.append((self.cohText, (self.rectMid, self.sliderCoh._y-20)))
        self.widgetList.append((self.radText, (self.rectMid, self.sliderRad._y-20)))
        self.widgetList.append((self.boidCountText, (self.rectMid, self.sliderBoidCount._y-20)))
        self.widgetList.append((self.dragText, (self.rectMid, self.sliderDrag._y-20)))

#Toggles and text--------------------------------------------------------------------------------------------
        self.edgesToggle = Toggle(window, int(self.rectMid), self.rect.y+self.widgetSpacing*7, 20, 10, 
                                    startOn=True, onColour=(0,234,0), handleOnColour=(255,255,255), handleOffColour=(255,255,255))
        self.debugToggle = Toggle(window, int(self.rectMid), self.rect.y+self.widgetSpacing*8, 20, 10, 
                                    startOn=False, onColour=(0,234,0), handleOnColour=(255,255,255), handleOffColour=(255,255,255))
        self.debugToggleVRect = Toggle(window, int(self.rectMid), self.rect.y+self.widgetSpacing*9, 20, 10, 
                                    startOn=False, onColour=(0,234,0), handleOnColour=(255,255,255), handleOffColour=(255,255,255))
        self.debugToggleQuadTree = Toggle(window, int(self.rectMid), self.rect.y+self.widgetSpacing*10, 20, 10, 
                                    startOn=False, onColour=(0,234,0), handleOnColour=(255,255,255), handleOffColour=(255,255,255))
        self.debugToggleParams = Toggle(window, int(self.rectMid), self.rect.y+self.widgetSpacing*11, 20, 10, 
                                    startOn=False, onColour=(0,234,0), handleOnColour=(255,255,255), handleOffColour=(255,255,255))

        self.edgesText = self.font.render('Avoid edges', True, (255, 255, 255))
        self.debugText = self.font.render('Show debug info', True, (255, 255, 255))
        self.debugTextVRect = self.font.render('Show vision radius of each boid', True, (255, 255, 255))
        self.debugTextQuadTree = self.font.render('Show quad tree', True, (255, 255, 255))
        self.debugTextParams = self.font.render('Show FPS and Boid count', True, (255, 255, 255))

        self.widgetList.append((self.edgesText, (self.rectMid+self.rectMid*0.05, self.edgesToggle._y)))
        self.widgetList.append((self.debugText, (self.rectMid+self.rectMid*0.05, self.debugToggle._y)))
        self.debugWidgetList.append((self.debugTextVRect, (self.rectMid+self.rectMid*0.05, self.debugToggleVRect._y)))
        self.debugWidgetList.append((self.debugTextQuadTree, (self.rectMid+self.rectMid*0.05, self.debugToggleQuadTree._y)))
        self.debugWidgetList.append((self.debugTextParams, (self.rectMid+self.rectMid*0.05, self.debugToggleParams._y)))

        self.debugToggleVRect.hide()
        self.debugToggleQuadTree.hide()
        self.debugToggleParams.hide()


    def draw(self, window, visibleUI, debugVisible, quadTree, flock):

        if self.debugToggleQuadTree.value:
            quadTree.draw(window)

        if self.debugToggleVRect.value:
            pygame.draw.rect(window, "white", flock[-1].rect, 2)
            pygame.draw.rect(window, "white", flock[-1].vRect, 2)   

        if self.debugToggleParams.value:
            if len(flock) != 0:
                pygame.font.init()
                font = pygame.font.SysFont(None, 24)
                fpsStr = str(int(clock.get_fps()))
                fps = font.render(fpsStr, True, (255, 255, 255))
                boidCountStr = str(len(flock))
                boidCount = font.render(boidCountStr, True, (255, 255, 255))
                window.blit(fps, (window.get_width() - 50, 50))
                window.blit(boidCount, (window.get_width() - 100, 50))

        if visibleUI:
            self.UIbackground.fill((100,100,100,128))
            window.blit(self.UIbackground, self.rect)
            self.sliderSep.show()
            self.sliderAlign.show()
            self.sliderCoh.show()
            self.sliderRad.show()
            self.sliderBoidCount.show()
            self.sliderDrag.show()

            self.edgesToggle.show()
            self.debugToggle.show()

            window.blits(self.widgetList)

            if debugVisible:
                window.blits(self.debugWidgetList)
                self.debugToggleVRect.show()
                self.debugToggleQuadTree.show()
                self.debugToggleParams.show()
            else:
                self.debugToggleVRect.hide()
                self.debugToggleQuadTree.hide()
                self.debugToggleParams.hide()

        else:
            self.sliderSep.hide()
            self.sliderAlign.hide()
            self.sliderCoh.hide()
            self.sliderRad.hide()
            self.sliderBoidCount.hide()
            self.sliderDrag.hide()

            self.edgesToggle.hide()
            self.debugToggle.hide()
            self.debugToggleVRect.hide()
            self.debugToggleQuadTree.hide()
            self.debugToggleParams.hide()
    

