import pygame

from tile import *
from settings import *
from player import *
from debug import debug
from support import *
from random import choice
from weapon import *
from ui import *

class level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.weapon_attack = None
        self.obstacle_sprites = pygame.sprite.Group()
        self.createmap()
        self.ui = ui()

    def createmap(self):
        layout = {
            'boundary':read_csv("./map/map_FloorBlocks.csv"),
            'grass' : read_csv("./map/map_Grass.csv"),
            'objects' : read_csv("./map/map_LargeObjects.csv"),
            }
        graphics = {
            "grass": import_folder("./graphics/grass/"),
            "objects": import_folder("./graphics/objects/"),
        }
        animations = {
            'up': import_folder('./graphics/player/up/'),'down': import_folder('./graphics/player/down/'),'left': import_folder('./graphics/player/left/'),'right': import_folder('./graphics/player/right/'),
            'up_idle': import_folder('./graphics/player/up_idle/'),'down_idle': import_folder('./graphics/player/down_idle/'),'left_idle': import_folder('./graphics/player/left_idle/'),'right_idle': import_folder('./graphics/player/right_idle/'),
            'up_attack': import_folder('./graphics/player/up_attack/'),'down_attack': import_folder('./graphics/player/down_attack/'),'left_attack': import_folder('./graphics/player/left_attack/'),'right_attack': import_folder('./graphics/player/right_attack/')
        }
        for style, layout in layout.items():
            for rowin,row in enumerate(layout):
                for colin,col in enumerate(row):
                    if col != '-1':
                        x = colin*tilesize
                        y = rowin*tilesize
                        if style == 'boundary':
                            tile((x,y),[self.obstacle_sprites],"invisible")
                        if style == 'grass':
                            img = choice(graphics['grass'])
                            tile((x,y),[self.visible_sprites,self.obstacle_sprites],'grass',img)
                        if style == 'objects':
                            img = graphics['objects'][int(col)]
                            tile((x,y),[self.visible_sprites,self.obstacle_sprites],'objects',img)
        self.player = player((2000,1430),[self.visible_sprites],self.obstacle_sprites,animations,self.attack,self.destroy_weapon)
        
    
    def attack(self,weapons):
        graphics = {
        "axe": {"cooldown":300,
                    "damage":30,
                    "images":import_folder("./graphics/weapons/axe/")},
            "lance": {"cooldown":400,
                    "damage":40,
                    "images":import_folder("./graphics/weapons/lance/")},
            "sword": {"cooldown":100,
                    "damage":20,"images":import_folder("./graphics/weapons/sword/")},
            "sai": {"cooldown":80,
                    "damage":15,"images":import_folder("./graphics/weapons/sai/")},
            "rapier": {"cooldown":50,
                    "damage":10,"images":import_folder("./graphics/weapons/rapier/")}
        }
        self.weapon_attack = weapon([self.visible_sprites],self.player,graphics[weapons])
    
    def destroy_weapon(self):
        if self.weapon_attack:
            #destroy weapon 
            self.weapon_attack.kill()
        self.weapon_attack = None
    
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surfaces = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_width = self.display_surfaces.get_width()//2
        self.half_height = self.display_surfaces.get_height()//2 
        self.map_surf = pygame.image.load("./graphics/tilemap/ground.png").convert_alpha()
        self.floor_rect = self.map_surf.get_rect(topleft=(0,0)) 
        

    def custom_draw(self,player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        map_surf_offset = self.floor_rect.topleft - self.offset
        self.display_surfaces.blit(self.map_surf,map_surf_offset)
        
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset 
            self.display_surfaces.blit(sprite.image,offset_pos)


