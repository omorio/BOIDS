import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.toggle import Toggle
from pygame_widgets.button import Button

initialSep = 2.0
initialAlign = 0.8
initialCoh = 0.5

class UI:
    def __init__(self, window, width, height):
        self.width = width
        self.height = height
        self.widgetSpacing = 50
        self.rect = pygame.Rect(8*self.width/10, self.height/10, 6*self.width/8, 8*self.height/10)
        self.rightPadding = 7.5*(self.width - self.rect.x)/10
        self.rectMid = self.rect.x + self.rightPadding/6
        self.UIbackground = pygame.Surface((self.width/5, 8*self.height/10), pygame.SRCALPHA)
        self.widgetList = []
#Sliders and text for boids----------------------------------------------------------------------------------
        self.sliderSep = Slider(window, self.rectMid, self.rect.y+self.widgetSpacing, self.rightPadding, 20, 
                                min=0, max=3, step=0.01, initial=initialSep)
        self.sliderAlign = Slider(window, self.rectMid, self.rect.y+self.widgetSpacing*2, self.rightPadding, 20, 
                                  min=0, max=1, step=0.01, initial=initialAlign)
        self.sliderCoh = Slider(window, self.rectMid, self.rect.y+self.widgetSpacing*3, self.rightPadding, 20, 
                                min=0, max=1, step=0.01, initial=initialCoh)
        self.sliderRad = Slider(window, self.rectMid, self.rect.y+self.widgetSpacing*4, self.rightPadding, 20, 
                                min=20, max=100, step=2, initial=60)
        
        self.font = pygame.font.SysFont(None, 24)

        self.sepText = self.font.render('Seperation', True, (255,255,255))
        self.alignText = self.font.render('Alignment', True, (255,255,255))
        self.cohText = self.font.render('Cohesion', True, (255,255,255))
        self.radText = self.font.render('Vision radius', True, (255,255,255))

        self.widgetList.append((self.sepText, (self.rectMid, self.sliderSep._y-20)))
        self.widgetList.append((self.alignText, (self.rectMid, self.sliderAlign._y-20)))
        self.widgetList.append((self.cohText, (self.rectMid, self.sliderCoh._y-20)))
        self.widgetList.append((self.radText, (self.rectMid, self.sliderRad._y-20)))
#Toggles and text--------------------------------------------------------------------------------------------
        self.edgesToggle = Toggle(window, int(self.rectMid), self.rect.y+self.widgetSpacing*5, 20, 10, 
                                  startOn=True, onColour=(0,234,0), handleOnColour=(255,255,255), handleOffColour=(255,255,255))
        self.debugToggle = Toggle(window, int(self.rectMid), self.rect.y+self.widgetSpacing*6, 20, 10, 
                                  startOn=False, onColour=(0,234,0), handleOnColour=(255,255,255), handleOffColour=(255,255,255))

        self.edgesText = self.font.render('Avoid edges', True, (255, 255, 255))
        self.debugText = self.font.render('Show debug info', True, (255, 255, 255))

        self.widgetList.append((self.edgesText, (self.rectMid+self.rectMid*0.05, self.edgesToggle._y)))
        self.widgetList.append((self.debugText, (self.rectMid+self.rectMid*0.05, self.debugToggle._y)))
#Sliders and text for chaser boids---------------------------------------------------------------------------
        #self.chaserSliderSep = Slider(window, self.rectMid, self.rect.y+self.widgetSpacing*7, self.rightPadding, 20, 
        #                        min=0, max=1, step=0.01, initial=initialSep)
        #self.chaserSliderAlign = Slider(window, self.rectMid, self.rect.y+self.widgetSpacing*8, self.rightPadding, 20, 
        #                          min=0, max=1, step=0.01, initial=initialAlign)
        #self.chaserSliderCoh = Slider(window, self.rectMid, self.rect.y+self.widgetSpacing*9, self.rightPadding, 20, 
        #                        min=0, max=1, step=0.01, initial=initialCoh)
        #self.chaserSliderRad = Slider(window, self.rectMid, self.rect.y+self.widgetSpacing*10, self.rightPadding, 20, 
        #                        min=40, max=200, step=2, initial=125)
        
        #self.ChaserSepText = self.font.render('Chaser Seperation', True, (255,255,255))
        #self.ChaserAlignText = self.font.render('Chaser Alignment', True, (255,255,255))
        #self.ChaserCohText = self.font.render('Chaser Cohesion', True, (255,255,255))
        #self.ChaserRadText = self.font.render('Chaser Vision radius', True, (255,255,255))

        #self.widgetList.append((self.ChaserSepText, (self.rectMid, self.chaserSliderSep._y-20)))
        #self.widgetList.append((self.ChaserAlignText, (self.rectMid, self.chaserSliderAlign._y-20)))
        #self.widgetList.append((self.ChaserCohText, (self.rectMid, self.chaserSliderCoh._y-20)))
        #self.widgetList.append((self.ChaserRadText, (self.rectMid, self.chaserSliderRad._y-20)))

#Button to delete chasers------------------------------------------------------------------------------------
        #self.delChaserButton = Button(
        #    # Mandatory Parameters
        #    window,  # Surface to place button on
        #    self.rectMid,  # X-coordinate of top left corner
        #    self.rect.y+self.widgetSpacing*11,  # Y-coordinate of top left corner
        #    self.rightPadding,  # Width
        #    50,  # Height

        #    # Optional Parameters
        #    text='Delete Chasers',  # Text to display
        #    fontSize=30,  # Size of font
        #    margin=20,  # Minimum distance between text/image and edge of button
        #    inactiveColour=(230, 230, 230),  # Colour of button when not being interacted with
        #    hoverColour=(200, 200, 200),  # Colour of button when being hovered over
        #    pressedColour=(230, 230, 230),  # Colour of button when being clicked
        #    radius=5,  # Radius of border corners (leave empty for not curved)

        #    )

    
    def draw(self, window, visible, visibleMargin, margin):
        if visible:
            if visibleMargin:
                pygame.draw.rect(window, "red", pygame.Rect(margin, margin , self.width - margin*2, self.height - margin*2), 2)
            self.UIbackground.fill((100,100,100,128))
            window.blit(self.UIbackground, self.rect)
            self.sliderSep.show()
            self.sliderAlign.show()
            self.sliderCoh.show()
            self.sliderRad.show()

            self.edgesToggle.show()
            self.debugToggle.show()

            #self.chaserSliderSep.show()
            #self.chaserSliderAlign.show()
            #self.chaserSliderCoh.show()
            #self.chaserSliderRad.show()

            #self.delChaserButton.show()

            window.blits(self.widgetList)
            
        else: 
            #if visibleMargin:
                #pygame.draw.rect(window, "red", pygame.Rect(margin*8, margin*8 , self.width - margin*2*8, self.height - margin*2*8), 2)
            self.sliderSep.hide()
            self.sliderAlign.hide()
            self.sliderCoh.hide()
            self.sliderRad.hide()

            self.edgesToggle.hide()
            self.debugToggle.hide()
        
            #self.chaserSliderSep.hide()
            #self.chaserSliderAlign.hide()
            #self.chaserSliderCoh.hide()
            #self.chaserSliderRad.hide()

            #self.delChaserButton.hide()

