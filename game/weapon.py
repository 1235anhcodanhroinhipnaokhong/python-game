import pygame
import math
from game.bullet import LineBullet
from game.settings import *
import random
from game.ultis.func  import TimerCallback, distance
from game.ultis.resource_loader import get_sprite_from_sheet

class Weapon(pygame.sprite.Sprite):
    sprite_groups = None
    obtacles = None
    @classmethod
    def init(cls, sprite_groups, obtacles): #! call this func before create any object
        cls.sprite_groups = sprite_groups
        cls.obtacles = obtacles
        
    def __init__(self, owner, sound_channel, name="" ,sound_init = True):
        super().__init__(self.sprite_groups)
        self.name = name
        self.owner = owner
        self.sound_channel = sound_channel
        self.type = "single"
        if sound_init:
            self.fire_sound = pygame.mixer.Sound(f"./assets/sounds/weapons/{self.name}.wav")
            self.fire_sound.set_volume(10)
        self.org_image = pygame.image.load(f"./assets/gfx/weapons/{self.name}.bmp").convert_alpha()
        self.image = self.org_image
        self.rect = self.image.get_rect()
        self.offset_x = 0
        self.offset_y = 0
        self.angle = 0
        self.dmg = 0
        self.pos_buffer = 32
        
    def rotate(self, angle):
        self.angle = -angle
        self.offset_x = math.cos(self.angle * (2 * math.pi / 360)) * self.pos_buffer
        self.offset_y = math.sin(self.angle * (2 * math.pi / 360)) * self.pos_buffer
        self.image = pygame.transform.rotate(self.org_image, angle)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.owner.hitbox.centerx + self.offset_x
        self.rect.centery = self.owner.hitbox.centery + self.offset_y 
        
    def fire(self):
        pass

    def stop(self):
        pass
    
    def update():
        pass
    
    

class Gun(Weapon):
    bullets_groups = None
    bullets_data = None
    
    @classmethod
    def init(cls, bullets_groups):
        cls.bullets_groups  = bullets_groups
    
    def __init__(self, owner , sound_channel, name = "ak47"):
        super().__init__(owner,sound_channel, name)
        self.gun_attr_init()
        self.reload_start_sound = pygame.mixer.Sound("./assets/sounds/weapons/reloadstart.wav")
        self.reload_end_sound = pygame.mixer.Sound("./assets/sounds/weapons/reloadend.wav")
        self.fire_cooldown = self.fire_rate
        self.reload_time_cnt = self.reload_time
        self.recoil_cnt = 0
        self.reloading = False
    
    def gun_attr_init(self):
        if self.name == "ak47":            
            self.type = "auto"
            self.fire_rate = 0.12
            self.recoil = 6
            self.max_bullets = 30
            self.reload_time = 3
            self.dmg = 25
            self.recoil_increase = 1
            
        elif self.name == "m4a1":
            self.type = "auto"
            self.fire_rate = 0.11
            self.recoil = 4
            self.max_bullets = 30
            self.reload_time = 3
            self.dmg = 24
            self.recoil_increase = 0.8
            
        elif self.name == "glock18":
            self.type = "single"
            self.fire_rate = 0.1
            self.recoil = 0
            self.max_bullets = 21
            self.reload_time = 3
            self.dmg = 11
            self.recoil_increase = 1
            
        elif self.name == "usp":
            self.type = "single"
            self.fire_rate = 0.1
            self.recoil = 0
            self.max_bullets = 12
            self.reload_time = 3
            self.dmg = 15
            self.recoil_increase = 1
        else :
            self.type = "auto"
            self.fire_rate = 0.1
            self.recoil = 5
            self.max_bullets = 30
            self.reload_time = 1
            self.dmg = 10
        self.bullets_remain = self.max_bullets
        
    def fire(self):
        if self.bullets_remain == 0 or self.reloading:
            return
        if self.type == "auto":
            if self.fire_cooldown > 0:
                return
            if self.fire_cooldown > -self.fire_rate:
                if int(self.recoil_cnt) != 0:
                    recoil = random.randrange(int(-self.recoil_cnt), int(self.recoil_cnt))
                else:
                    recoil = 0
                if self.recoil_cnt < self.recoil:
                    self.recoil_cnt += self.recoil_increase
            else:
                recoil = 0
                self.recoil_cnt = 0
        elif self.type == "single":
            recoil = 0
            
        self.fire_cooldown = self.fire_rate
        self.sound_channel.play(self.fire_sound)
        self.bullets_remain -= 1
        new_bullet = LineBullet(self.owner.hitbox.center, self.angle + recoil, self.owner.id, self.dmg)
        self.bullets_groups.append(new_bullet)
        self.owner.bullets.append(new_bullet.to_object_value())
    
    def reset(self):
        self.bullets_remain = self.max_bullets

    def reload(self):
        self.reloading = True
            
    def update(self):
        self.fire_cooldown -= 1 / FPS
        if self.bullets_remain == 0 or self.reloading:
            if self.reload_time_cnt == self.reload_time:
                self.sound_channel.play(self.reload_start_sound)
            if abs(int(self.reload_time_cnt * 100) - 150) <= 100 / FPS:
                self.sound_channel.play(self.reload_end_sound)
            self.reload_time_cnt -= 1 / FPS
            if self.reload_time_cnt <= 0:
                self.reload_time_cnt = self.reload_time
                self.bullets_remain = self.max_bullets
                self.reloading = False
            


class Knife(Weapon):
    def __init__(self, owner, sound_channel):
        super().__init__(owner,sound_channel , 'knife')
        self.type = "auto"
        self.slash_cooldown = 0
        self.slash_delay = 0.4
    
    def fire(self):
        if self.slash_cooldown > 0:
            return
        (x, y) = self.rect.topleft
        net_data = [x, y, self.rect.width, self.rect.height, self.owner.id]
        self.owner.knife_sl.append(net_data)
        self.slash_cooldown = 0.4
        self.sound_channel.play(self.fire_sound)
        self.owner.onslash = True
        self.owner.knife_slash_animation()  
    
    def reset(self):
        self.slash_cooldown = self.slash_delay    
        
    def update(self, *args, **kwargs):
        if self.slash_cooldown > 0:
            self.slash_cooldown -= 1 / FPS




class Grenade(Weapon):    
    def __init__(self, owner,sound_channel, name = "he"):
        super().__init__(owner,sound_channel, name, False)
        self.bullets_remain = 3
        self.grenade_init()
        self.pos_buffer = 22
        self.throw_time = 2.2
        self.throw_time_cnt = self.throw_time
        self.angle = 0
        self.onthrow = False
    
    
    def grenade_init(self):
        if self.name == "he":
            self.dmg = 50
         
    def reset(self):
        self.bullets_remain = 3     
        if self not in self.sprite_groups:
            self.sprite_groups.add(self)
        self.onthrow = False
        self.throw_time_cnt = self.throw_time
        
    def rotate(self, angle):
        self.angle = angle
        super().rotate(angle)
    
    def fire(self):
        self.onthrow = True
        if self.throw_time_cnt == self.throw_time and self.bullets_remain > 0:
            ThrowGrenadeObject(self.owner, self.sprite_groups, self.angle, self.rect.center, self.obtacles)
            self.bullets_remain -= 1
    
    def finish_throw(self):        
        self.onthrow = False
        self.explode_img_index = 0
        self.throw_time_cnt = self.throw_time
        if self.bullets_remain == 0:
            self.owner.switch_to_primary_weapon()
            self.sprite_groups.remove(self)
    

                
    def update(self):
        if self.onthrow:
            self.throw_time_cnt -= 1/FPS
            if self.throw_time_cnt <= 0:
                self.finish_throw()
        

class ThrowGrenadeObject(pygame.sprite.Sprite):
    def __init__(self,owner, sprite_groups ,angle , pos, obtacles):
        super().__init__(sprite_groups)
        self.sprite_groups = sprite_groups
        self.obtacles = obtacles
        self.explode_sound = pygame.mixer.Sound("./assets/sounds/weapons/explode1.wav")
        self.org_image = pygame.image.load(f"./assets/gfx/weapons/he.bmp").convert_alpha()
        self.image = self.org_image
        self.rect = self.image.get_rect(center = pos)
        self.throw_speed = 10
        self.throw_time_cnt = 2.2
        self.hitbox = self.rect.inflate((-25,-25))
        self.explode_img_sheet = pygame.transform.scale(pygame.image.load("./assets/gfx/explosion.png"),(640,640))
        self.explode_img_index = 0
        self.data_send = False
        self.owner = owner
        
        self.speed_x = math.cos(angle * (2 * math.pi / 360)) * self.throw_speed
        self.speed_y = math.sin(angle * (2 * math.pi / 360)) * self.throw_speed
      
    def finish_throw(self):        
        self.explode_img_index = 0
        self.data_send = False
        self.sprite_groups.remove(self)
        self.kill()
    
    def handle_collision(self):
        for obtacle in sorted(self.obtacles, key = lambda x : distance(self.hitbox.center, x.rect.center)):
                if obtacle.rect.colliderect(self.hitbox):
                    dx = self.hitbox.centerx - obtacle.rect.centerx
                    dy = self.hitbox.centery - obtacle.rect.centery
                    if abs(dx) > abs(dy): 
                        if dx > 0:
                            if self.speed_x < 0:
                                self.speed_x = -self.speed_x
                        else:
                            if self.speed_x > 0:
                                self.speed_x = -self.speed_x
                    else:  
                        if dy > 0:
                            if self.speed_y < 0:
                                self.speed_y = -self.speed_y
                        else:
                            if self.speed_y > 0:
                                self.speed_y = -self.speed_y
                    break
        
    def update(self):
        self.hitbox.center = self.rect.center
        self.throw_time_cnt -= 1/FPS               
        self.handle_collision()
        if abs(int(self.throw_time_cnt * 100) - 60 * 2.5) <= 100 / FPS:
            self.owner.sound_channel.play(self.explode_sound)
                        
        if self.throw_time_cnt >= 0.42 * 2.5:
            self.rect.centerx += self.speed_x
            self.rect.centery += self.speed_y
        else:
            if not self.data_send:
                self.data_send = True
                self.owner.explode_nade.append((self.rect.centerx, self.rect.centery, self.owner.id))
            self.image = get_sprite_from_sheet(self.explode_img_sheet, 128, int(self.explode_img_index))
            self.explode_img_index += 1/2.5
            if self.explode_img_index > 24:
                self.explode_img_index = 24
            
        if self.throw_time_cnt <= 0:
            self.finish_throw()