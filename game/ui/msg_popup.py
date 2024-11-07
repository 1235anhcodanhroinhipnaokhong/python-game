import pygame
import threading



class MsgPopup:
    def __init__(self, pos, size, msg = "", font_size = 25):
        self.width, self.height = size
        self.surf = pygame.Surface(size)
        self.pos = pos
        self.msg = msg
        self.bg_color = (50, 50 ,50)
        self.surf.set_alpha(125)
        self.font = pygame.font.Font('assets/fonts/korean.ttf', font_size) 
        self.text_surf = self.font.render(msg, True, (255, 255, 255))
        self.text_rect = self.text_surf.get_rect(center = (self.width / 2, self.height/2))
        self.display_surf = pygame.display.get_surface()
        self.twin_sound = pygame.mixer.Sound("./assets/sounds/terwin.ogg")
        self.ctwin_sound = pygame.mixer.Sound("./assets/sounds/ctwin.ogg")
    
    def clear(self):
        self.msg = ""    
        
    def update(self, msg = ""):
        if msg != "" and msg != self.msg:
            self.msg = msg
            self.text_surf = self.font.render(msg, True, (255, 255, 255))
            self.text_rect = self.text_surf.get_rect(center = (self.width / 2, self.height/2))
            if msg == "Terrorists Win":
                self.twin_sound.play()
            if msg == "Counter-Terrorists Win":
                self.ctwin_sound.play()
            timer = threading.Timer(3, self.clear)
            timer.start()
            
    def display(self):
        if self.msg != "":
            self.surf.fill(self.bg_color)
            self.surf.blit(self.text_surf, self.text_rect)
            self.display_surf.blit(self.surf, self.pos)
        
        
    
    
    