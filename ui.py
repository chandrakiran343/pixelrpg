import pygame
from settings import *

class ui:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(uiFont, uiFontSize)

        #bar setup
        self.healthbar = pygame.Rect(10,10,healthbarWidth,barHeight)
        self.energybar = pygame.Rect(10,34,energybarWidth,barHeight)

    def showBar(self,current,max,bgrect,color):
        pygame.draw.rect(self.display_surface,uibgColor,bgrect)

        #convert
        ratio = current/max
        bar_width = (ratio*bgrect.width)
        bar = bgrect.copy()
        bar.width = bar_width
        #draw bar
        pygame.draw.rect(self.display_surface,color,bar)
        pygame.draw.rect(self.display_surface,uiborderColor,bgrect,3)

    def showExp(self,exp):
        exp_surf = self.font.render(str(int(exp)),True,textColor)
        exp_rect = exp_surf.get_rect(bottomright = (self.display_surface.get_width()-20,self.display_surface.get_height()-20))
        pygame.draw.rect(self.display_surface, uibgColor, exp_rect.inflate(10,10))
        self.display_surface.blit(exp_surf,exp_rect)
        pygame.draw.rect(self.display_surface, uibgColor, exp_rect.inflate(10,10),3)
    def display(self,player):
        self.player = player
        self.player.health = 90
        # pygame.draw.rect(self.display_surface, uibgColor, self.healthbar)
        # pygame.draw.rect(self.display_surface, uibgColor, self.energybar)
        self.showBar(self.player.health,self.player.stats['health'],self.healthbar,healthbarColor)
        self.showBar(self.player.mana,self.player.stats['mana'],self.energybar,energybarColor)
        self.showExp(self.player.exp)