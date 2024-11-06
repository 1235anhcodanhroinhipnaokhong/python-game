import pygame
import random

class SelectMenu:

    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('assets/fonts/korean.ttf', 20)  
        self.main_active = True 
        self.terrorists_menu_active = False
        self.counter_terrorists_menu_active = False
        
        self.menu_rect = pygame.Rect(0, 0, 600, 400)
        self.menu_rect.center = (self.display_surface.get_width() // 2, self.display_surface.get_height() // 2)

        self.main_buttons = self.create_main_buttons()
        self.terrorists_buttons = self.create_terrorists_menu_buttons()
        self.counter_terrorists_buttons = self.create_counter_terrorists_menu_buttons()
        
        self.buttons = self.create_main_buttons()
        self.done = False
        self.val = ""
        

    def create_main_buttons(self):
        main_buttons = {
            "Terrorists": pygame.Rect(0, 0, 300, 50),
            "Counter-Terrorists": pygame.Rect(0, 0, 300, 50),
            "Close": pygame.Rect(0, 0, 300, 50),
        }

        
        y_start = self.menu_rect.top + 50
        for i, rect in enumerate(main_buttons.values()):
            rect.centerx = self.menu_rect.centerx
            rect.y = y_start + i * 70 

        return main_buttons

    def create_terrorists_menu_buttons(self):
        
        terrorists_buttons = {
            "1. Phoenix Connexion": pygame.Rect(0, 0, 300, 50),
            "2. L337 Krew": pygame.Rect(0, 0, 300, 50),
            "3. Arctic Avengers": pygame.Rect(0, 0, 300, 50),
            "4. Guerilla Warfare": pygame.Rect(0, 0, 300, 50),
            "5. Auto-Select": pygame.Rect(0, 0, 300, 50),
        }
        y_start = self.menu_rect.top + 50
        for i, rect in enumerate(terrorists_buttons.values()):
            rect.centerx = self.menu_rect.centerx
            rect.y = y_start + i * 60
        return terrorists_buttons
        
    def create_counter_terrorists_menu_buttons(self):
        counter_terrorists_buttons = {
            "1. SEAL Team 6": pygame.Rect(0, 0, 300, 50),
            "2. GSG 9": pygame.Rect(0, 0, 300, 50),
            "3. SAS": pygame.Rect(0, 0, 300, 50),
            "4. GIGN": pygame.Rect(0, 0, 300, 50),
            "5. Auto-Select": pygame.Rect(0, 0, 300, 50),
        }
        y_start = self.menu_rect.top + 50
        for i, rect in enumerate(counter_terrorists_buttons.values()):
            rect.centerx = self.menu_rect.centerx
            rect.y = y_start + i * 60
        return counter_terrorists_buttons
    def toggle(self):
        self.main_active = not self.main_active

    def draw(self):
        if self.main_active:
            self.draw_menu()

    def draw_menu(self):        
            s = pygame.Surface((self.display_surface.get_width(), self.display_surface.get_height()))
            s.set_alpha(0)  
            s.fill((190,158,108))
            self.display_surface.blit(s, (0, 0))
            
            menu_surface = pygame.Surface(self.menu_rect.size)
            menu_surface.fill((50, 50, 50)) 
            menu_surface.set_alpha(128)  
            self.display_surface.blit(menu_surface, self.menu_rect.topleft)
            pygame.draw.rect(self.display_surface, (255, 255, 255), self.menu_rect, 2, border_radius=10)

            mouse_pos = pygame.mouse.get_pos()
            for name, rect in self.buttons.items():
                color = (100, 100, 100)  
                if rect.collidepoint(mouse_pos):
                    color = (150, 150, 150)

                pygame.draw.rect(self.display_surface, color, rect, border_radius=10)
                text_surf = self.font.render(name, True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=rect.center)
                self.display_surface.blit(text_surf, text_rect)

    def handle_event(self, event : pygame.event.EventType):
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:  
            self.val = ""
            self.toggle()
            self.buttons = self.main_buttons
        
        if event.type == pygame.MOUSEBUTTONDOWN and self.main_active and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for name, rect in self.buttons.items():
                if rect.collidepoint(mouse_pos):
                    if name == 'Terrorists' :
                        self.buttons = self.terrorists_buttons
                        self.val = "t"
                    elif name == 'Counter-Terrorists' :
                        self.buttons = self.counter_terrorists_buttons
                        self.val = "ct"
                    elif name == 'Close':
                        self.toggle()
                    else:
                        num = int(name[0])
                        if num == 5:
                            num = random.randrange(1,4)
                        self.val += str(num)
                        self.toggle()