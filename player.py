import pygame
from settings import *
from debug import debug
import time
from random import choice

class player(pygame.sprite.Sprite):
    def __init__(self,pos,group,obstacle_sprites,animations,attack,destroy):
        super().__init__(group)
        self.image = pygame.image.load('./graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 3
        self.obstacle_sprites = obstacle_sprites
        self.hitbox = self.rect.inflate(0,-26)
        self.attacking = False
        self.cooldowns = 400
        self.animations = animations
        self.attack_time = None
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.time = pygame.time.get_ticks()
        self.attack = attack
        self.list = ["axe","lance","rapier","sai","sword"]
        self.index = 0
        self.weapon = self.list[self.index]
        self.destroy = destroy
        self.switch_weapon = True
        self.switch_weapon_time = None
        self.switch_duration = 200
        self.stats = {'health':100,'mana':100,'strength':10,'agility':10,'intelligence':10}
        self.health = self.stats['health']
        self.mana = self.stats['mana']
        self.exp = 123
        
    

    def animate(self):

        if self.direction.x == 0 and self.direction.y == 0 and '_idle' not in self.status and not self.attacking:
            if '_attack' in self.status:
                self.status = self.status.replace('_attack','_idle')
            else:
                self.status += '_idle'
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if '_attack' not in self.status:
                if '_idle' in self.status:
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status += '_attack'
        animate = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animate):
            self.frame_index = 0
        self.image = animate[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = +1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = +1
                self.status = 'right'
            else:
                self.direction.x = 0
            
            if keys[pygame.K_q] and self.switch_weapon:
                self.switch_weapon = False
                self.switch_weapon_time = pygame.time.get_ticks()
                self.index += 1
                if self.index >= len(self.list):
                    self.index = 0
                self.weapon = self.list[self.index]
                
            
            if (keys[pygame.K_SPACE] and not self.attacking):
                self.attack_time = pygame.time.get_ticks()
                self.attacking = True
                self.attack(self.weapon)
                
            if (keys[pygame.K_RCTRL] and not self.attacking ): 
                self.attack_time = pygame.time.get_ticks()
                self.attacking = True
            

            if abs(self.direction.x) == abs(self.direction.y) and self.direction.y != 0 and self.direction.y != +1:
                self.direction.x = 0
                self.direction.y = -1
                self.status = 'up'
            elif abs(self.direction.x) == abs(self.direction.y) and self.direction.y != 0 and self.direction.y == +1:
                self.direction.y = +1
                self.direction.x = 0
                self.status = 'down'

            if keys[pygame.K_w] and self.attacking or keys[pygame.K_UP] and self.attacking:
                self.direction.y = 0
            elif keys[pygame.K_s] and self.attacking or keys[pygame.K_DOWN] and self.attacking:
                self.direction.y = 0
            elif keys[pygame.K_a] and self.attacking or keys[pygame.K_LEFT] and self.attacking:
                self.direction.x = 0
            elif keys[pygame.K_d] and self.attacking or keys[pygame.K_RIGHT] and self.attacking:
                self.direction.x = 0
        
    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if (current_time - self.attack_time) >= self.cooldowns:
                self.attacking = False
                self.destroy()
        if not self.switch_weapon:
            if (current_time - self.switch_weapon_time) >= self.switch_duration:
                self.switch_weapon = True


    def collision(self,direction):
        if direction  == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top 
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
    
    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed     
        self.collision('vertical')  
        self.rect.center = self.hitbox.center
    
    def update(self):
        self.input()
        self.cooldown()
        self.move(self.speed)
        self.animate()