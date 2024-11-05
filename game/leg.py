import pygame, math
from game.ultis.resource_loader import *
from game.settings import *
class Leg(pygame.sprite.Sprite):
    sprite_group = None
    @classmethod
    def init(cls, groups):
        cls.sprite_group = groups
    
    def __init__(self, owner):
        super().__init__(self.sprite_group)
        self.owner = owner
        self.sprites_sheet = pygame.image.load("./assets/gfx/player/legs.bmp")
        self.img_list = []
        for i in range(0,16):
            self.img_list.append(get_sprite_from_sheet(self.sprites_sheet,64,i))
        self.org_image = self.img_list[0]
        self.curr_sp_index = 0
        self.max_sp = 16
        self.image = self.org_image
        self.rect = self.image.get_rect()
        self.walk_delay = 0.05
        self.time_cnt = 0
        self.offset_x = 0
        self.offset_y = 0
        self.angle = 0
        self.pos_buffer = -17
        
    def walk(self):
        if self.time_cnt <= 0:
            self.curr_sp_index += 2
            if self.curr_sp_index >= 16:
                if self.curr_sp_index % 2 == 0:
                    self.curr_sp_index = 17
                else:
                    self.curr_sp_index = 16
            self.curr_sp_index %= self.max_sp
            self.time_cnt = self.walk_delay
            # if self.curr_sp_index % 2 == 0:
            self.org_image = self.img_list[self.curr_sp_index]
    
    def change_index(self, index):
        self.org_image = self.img_list[self.curr_sp_index]
    
    def rotate(self, angle):
        self.angle = -angle
        self.offset_x = math.cos(self.angle * (2 * math.pi / 360)) * self.pos_buffer
        self.offset_y = math.sin(self.angle * (2 * math.pi / 360)) * self.pos_buffer
        self.image = pygame.transform.rotate(self.org_image, angle)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.owner.hitbox.centerx + self.offset_x
        self.rect.centery = self.owner.hitbox.centery + self.offset_y 
    
    def update(self):
        self.time_cnt -= 1/FPS
    