import pygame

class PauseMenu:

    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('assets/fonts/korean.ttf', 20)  
        self.active = False
        
        self.menu_rect = pygame.Rect(0, 0, 600, 400)
        self.menu_rect.center = (self.display_surface.get_width() // 2, self.display_surface.get_height() // 2)
        self.menu_surface = pygame.Surface(self.menu_rect.size)
        self.menu_surface.set_alpha(128)  
        
        self.disconnect_text = self.font.render("Disconnect", True, (255, 255, 255))
        self.disconnect_rect = pygame.Rect(self.menu_rect.left + 100,self.menu_rect.top + 60,400,80)
        self.disconnect_text_surf = self.disconnect_text.get_rect(center=self.disconnect_rect.center)
        
        self.cancel_text = self.font.render("Cancel", True, (255, 255, 255))
        self.cancel_rect = pygame.Rect(self.menu_rect.left + 100,self.menu_rect.top + 240,400,80)
        self.cancel_text_surf = self.cancel_text.get_rect(center=self.cancel_rect.center)
    
    def toggle(self):
        self.active = not self.active

    def draw(self):
        if self.active:
            self.draw_menu()
        

    def draw_menu(self):                    
            mouse_pos = pygame.mouse.get_pos()
            self.menu_surface.fill((50, 50, 50)) 
            self.menu_surface.set_alpha(128)  
            pygame.draw.rect(self.display_surface, (255, 255, 255), self.menu_rect, 2, border_radius=10)
            self.display_surface.blit(self.menu_surface, self.menu_rect.topleft)
            pygame.draw.rect(
                                self.display_surface,  
                                (150, 150, 150)  if self.disconnect_rect.collidepoint(mouse_pos) else (100, 100, 100), 
                                self.disconnect_rect
                                )
            pygame.draw.rect(
                                self.display_surface, 
                                (150, 150, 150)  if self.cancel_rect.collidepoint(mouse_pos) else (100, 100, 100),
                                self.cancel_rect 
                                )
            self.display_surface.blit(self.disconnect_text, self.disconnect_text_surf)
            self.display_surface.blit(self.cancel_text, self.cancel_text_surf)
