import pygame, sys
import random
from game.ui.input import InputBox

class StartMenu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.menu_font = pygame.font.Font('assets/fonts/liberationsans.ttf', 30)
        self.button_names = [
            "Create" , "Change Name" , "Join", "Quit"
        ]
        self.join_buttons_name = []
        
        self.buttons = []
        self.init_buttons()
        
        self.join_buttons = []
        self.default_name = "user" + str(random.randrange(10000, 100000))
        
        self.create = False
        self.join = False
        self.change_name = False
        self.addr = None
        self.hello_mf = self.menu_font.render(f"{self.default_name} is home!", True, (255, 255, 255))
        self.hello_rect = self.hello_mf.get_rect(topleft= (50,20))
        self.name_input = InputBox(370, 230, 700, 80)

    def init_buttons(self):
        y_start = 150
        for index, name in enumerate(self.button_names):
            if index == 3 :
                button_rect = pygame.Rect(50, y_start + index * 100, 285, 40)
            else :
                button_rect = pygame.Rect(50, y_start + index * 50, 285, 40)
            self.buttons.append((name, button_rect))
            
    def init_join_buttons(self, server_list):
        y_start = 150
        for index, server in enumerate(server_list):
            button_rect = pygame.Rect(370, y_start + index * 50, 285, 40)
            self.join_buttons.append((server[0], button_rect,server[1] ,server[2]))
            
    def draw(self):
        self.display_surface.fill((0, 0, 0))
        for name, rect in self.buttons:
            color = (200, 200, 200) if rect.collidepoint(pygame.mouse.get_pos()) else (100, 100, 100)
            pygame.draw.rect(self.display_surface, color, rect)
            text_surface = self.menu_font.render(name, True, (255, 255, 255))
            self.display_surface.blit(text_surface, (rect.x + 10, rect.y + 5))
        self.hello_mf = self.menu_font.render(f"{self.default_name} is home!", True, (255, 255, 255))
        self.hello_rect = self.hello_mf.get_rect(topleft= (50,20))
        self.display_surface.blit(self.hello_mf, self.hello_rect)
        self.draw_join()
        self.draw_change_name()
            
    def draw_join(self) :
        if self.join == True :
            for name, rect, host ,port in self.join_buttons:
                color = (200, 200, 200) if rect.collidepoint(pygame.mouse.get_pos()) else (100, 100, 100)
                pygame.draw.rect(self.display_surface, color, rect)
                text_surface = self.menu_font.render(name, True, (255, 255, 255))
                self.display_surface.blit(text_surface, (rect.x + 10, rect.y + 5))
                
    def draw_change_name(self) :
        if self.change_name == True :
            text_surface = self.menu_font.render("Type name", True, (255, 255, 255))
            text_rect = pygame.Rect(370, 150, 285, 40)
            color = (200, 200, 200) if text_rect.collidepoint(pygame.mouse.get_pos()) else (100, 100, 100)
            pygame.draw.rect(self.display_surface, color, text_rect)
            self.display_surface.blit(text_surface, (text_rect.x + 10, text_rect.y + 5))
            self.name_input.draw(self.display_surface)
            
    # def event_handle(self, event :pygame.event.EventType):
    #     if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            