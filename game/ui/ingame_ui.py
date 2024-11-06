import pygame
import time

class IngameUI:
    def __init__(self):
        # General
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('assets/fonts/digital-7.ttf', 60)
        
        # Countdown timer initialization
        self.start_time = time.time()
        self.countdown_seconds = 5 * 60  # 5 minutes in seconds

    def show_hp(self, hp):
        # hp_text_surf
        hp_text_render = self.font.render(str(int(hp)), False, (255,232,80))
        hp_text_rect = hp_text_render.get_rect()

        #hp_symbol
        hp_symbol_surf = pygame.transform.scale(pygame.image.load('assets/fonts/health.webp'), (55,55))
        hp_symbol_rect = hp_symbol_surf.get_rect()
        
        #hp_symbol_pos
        x = 20  
        y = self.display_surface.get_size()[1] - 20 
        hp_symbol_rect.bottomleft = (x, y)
        
        hp_text_rect.center = hp_symbol_rect.centerx + hp_symbol_rect.width + 20, hp_symbol_rect.centery
        
        
        self.display_surface.blit(hp_text_render, hp_text_rect)
        self.display_surface.blit(hp_symbol_surf, hp_symbol_rect)

    def show_timer(self, time):
        timer_text = time
        timer_text_render = self.font.render(timer_text, False, (255,232,80))  
        timer_rect = timer_text_render.get_rect()
        
        timer_symbol = pygame.transform.scale(pygame.image.load('assets/fonts/clock.png').convert_alpha(), (55, 55))
        timer_symbol_rect = timer_symbol.get_rect()

        
        x = self.display_surface.get_size()[0] // 2
        y = self.display_surface.get_size()[1] - 20 - timer_text_render.get_height()

        timer_rect.centerx = x  
        timer_rect.y = y

        
        timer_symbol_rect.midright = (timer_rect.midleft[0] - 20, timer_rect.midleft[1])

        
        self.display_surface.blit(timer_text_render, timer_rect)
        self.display_surface.blit(timer_symbol, timer_symbol_rect)

    def show_bullet(self, selected_weapon):
        if hasattr(selected_weapon, 'bullets_remain') :
            # bullet_text_surf
            bullet_text_render = self.font.render(str(int(selected_weapon.bullets_remain)), False, (255,232,80))
            bullet_text_rect = bullet_text_render.get_rect()
    
            #bullet_symbol
            bullet_symbol_surf = pygame.transform.scale(pygame.image.load('assets/fonts/bullet.png'), (55,55))
            bullet_symbol_rect = bullet_symbol_surf.get_rect()
            
            #bullet_symbol_pos
            x = self.display_surface.get_size()[0] - 20
            y = self.display_surface.get_size()[1] - 20 
            bullet_text_rect.bottomright = (x, y)
            
            bullet_symbol_rect.center = bullet_text_rect.centerx - bullet_text_rect.width - 20, bullet_text_rect.centery
            
            
            self.display_surface.blit(bullet_text_render, bullet_text_rect)
            self.display_surface.blit(bullet_symbol_surf, bullet_symbol_rect)
    
    def display(self, player, time):
        self.show_hp(player.hp)
        self.show_timer(time)  
        self.show_bullet(player.selected_weapon)
