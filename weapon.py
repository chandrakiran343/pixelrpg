from numpy import delete
import pygame

class weapon(pygame.sprite.Sprite):
    def __init__(self,group,player,data):
        super().__init__(group)
        self.direction = player.status.split('_')[0]
        self.player = player
        self.data = data
        if self.direction == 'right':
            self.image = data["images"][3]
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))
        elif self.direction == 'left':
            self.image = data["images"][2]
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16))
        elif self.direction == 'up':
            self.image = data["images"][4]
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-16,0))
        else:
            self.image = data["images"][0]
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-16,0))
            

    
        

