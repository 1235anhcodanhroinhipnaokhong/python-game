import pygame
import queue
import threading

class MessageBar:
    
    def __init__(self, pos, surf_size, msg_height):
        self.pos = pos
        self.height , self.width = surf_size
        self.msg_height = msg_height
        self.surf =pygame.Surface(surf_size)
        self.surf.convert_alpha()
        self.bg_color = (220,220,220)
        self.surf.fill(self.bg_color)
        self.surf.set_colorkey(self.bg_color)
        self.msg_list = []
        self.msg_components = []
        self.display_surf = pygame.display.get_surface()
   
    def add_message(self, msg):
        self.msg_list.append(msg)
        len = self.msg_list.__len__()
        self.msg_components.append(
            Label(msg, (self.width/2, self.msg_height * len), (255,255,255), True)
        )

    def pop_message(self):
        self.msg_list.pop(0)
        self.msg_components.pop(0)
        for index, msg_component in enumerate(self.msg_components):
            msg_component.place((self.width / 2, self.msg_height * index))

    def update(self, incomming_msg_list):
        for msg in incomming_msg_list:
            if msg not in self.msg_list:
                self.add_message(msg)
                timer = threading.Timer(3.5, self.pop_message)
                timer.start()
    
    def display(self):  
        self.display_surf.blit(self.surf, self.pos)
        self.surf.fill(self.bg_color)
        for msg_component in self.msg_components:
            msg_component.display(self.surf)


class Label:
    
    def __init__(self,text, pos, color, center = False, font_size = 20):
        self.text = text
        self.color = color
        self.pos = pos
        self.font = pygame.font.Font('assets/fonts/korean.ttf', font_size)
        # self.font = pygame.font.SysFont('firacode light', font_size)
        self.text_surf = self.font.render(self.text,0, self.color)
        if center:
            self.text_rect = self.text_surf.get_rect(center=pos)
        else:
            self.text_rect = self.text_surf.get_rect(topleft=pos)
    
    def place(self,pos):
        self.text_rect = self.text_surf.get_rect(center=pos)
    
    def display(self, surf):
        surf.blit(self.text_surf, self.text_rect)    