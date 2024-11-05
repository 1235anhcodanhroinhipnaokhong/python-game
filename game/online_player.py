import pygame
import random, math
from game.player import Player
from game.settings import *
from game.ultis.resource_loader import get_sprite_from_sheet
from game.weapon import Gun


class OnlinePlayer(Player):
    
    def __init__(self, spwan_pos, sprite_groups, obtacles_sprites, team="ct", id = ""):
        super().__init__(spwan_pos, sprite_groups, obtacles_sprites, team , id)
        self.speed = 5
        self.time = 0
        
    def handle_angle(self):
        self.image = pygame.transform.rotate(self.org_image, -self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.hitbox.center
        if self.selected_weapon:
            self.selected_weapon.rotate(-self.angle)
        self.leg.rotate(-self.angle)
    
    def load_data(self, data):
        if self.team != data['team']:
            self.team = data['team']
            self.switch_team(self.team)
        self.hitbox.center = data['pos']
        self.hp = data['hp']
        self.angle = data['angle']
        self.leg.curr_sp_index = data['leg_index']
        self.leg.change_index(self.leg.curr_sp_index)
        if self.dead != data['dead']:
            if data['dead'] == False:
                Gun.sprite_groups.add(self.selected_weapon)
            else:
                Gun.sprite_groups.remove(self.selected_weapon)
            self.dead = data['dead']
        
        if data['firing'] == True:
            self.fire()
            pass
        
        if self.selected_weapon_index != data['wp_index']:
            self.set_selected_weapon(self.weapons_list[data['wp_index']])
            self.selected_weapon_index = data['wp_index']
            
        if self.sprite_index != data['sp_index']:
            self.sprite_index = data['sp_index']
            if self.sprite_index == -1:
                self.org_image = self.dead_image
                self.image = self.org_image
                self.rect = self.image.get_rect()
                self.rect.center = self.hitbox.center
            else:
                self.org_image =  self.org_image = get_sprite_from_sheet(self.sprites_sheet, PLAYER_SIZE, self.sprite_index)
        
    def update(self):
        if not self.dead:
            self.handle_angle()       
