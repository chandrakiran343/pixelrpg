import pygame
from settings import *

class tile(pygame.sprite.Sprite):
    def __init__(self,pos,group,sprite_type,surface = pygame.Surface((tilesize,tilesize))):
        super().__init__(group)
        self.sprite_type = sprite_type
        self.image = surface
        if sprite_type == 'objects':
            self.rect = self.image.get_rect(topleft=(pos[0],pos[1] - tilesize))
            self.hitbox = self.rect.inflate(-10,-90)
        else:
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(-10,-10)