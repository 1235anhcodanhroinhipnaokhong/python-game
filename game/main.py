import pygame, sys, time
from pygame.locals import *
from game.settings import *
from game.gameclient import GameClient
from game.ui.button import Button
from game.ui.select_menu import SelectMenu
from game.ui.pause_menu import PauseMenu
from game.network import Network, HOST
from game.intro import Intro
from game.start_menu import StartMenu

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SRC_WIDTH, SRC_HEIGHT))
        pygame.display.set_caption("2D Shootting")
        self.clock = pygame.time.Clock()
        self.game_client = None
        self.events = NOEVENT
        
        self.font = pygame.font.Font('assets/fonts/digital-7.ttf', 30)
        self.select_menu = SelectMenu()
        self.network = Network()
        self.pause_menu = PauseMenu()
        
        
        
    
    def main_menu(self):
        self.main_menu_running = True  
        self.start_menu = StartMenu()
        def create_done():
            new_server_name = self.start_menu.server_name_input.text
            self.start_menu.server_name_input.text = ""
            self.start_menu.addr = self.network.create_new_server(new_server_name)
            self.main_menu_running = False
        
        def change_name_done():
            self.start_menu.default_name = self.start_menu.name_input.text
            self.start_menu.change_name = False
            
        while self.main_menu_running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == KEYDOWN and event.key == pygame.K_RETURN:
                    if self.start_menu.change_name:
                        change_name_done()
                        
                    if self.start_menu.create:
                        create_done()
                        
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for name, rect in self.start_menu.buttons:
                        if rect.collidepoint(mouse_pos):
                            if name == 'Create' :
                                self.start_menu.create = True
                                self.start_menu.change_name =False
                                self.start_menu.join = False
                                 
                            elif name == 'Join' :
                                self.start_menu.create = False
                                self.start_menu.change_name = False  
                                self.start_menu.join = True
                                self.start_menu.init_join_buttons(self.network.get_servers_list())
                                                     
                            elif name == 'Change Name' :
                                self.start_menu.create = False
                                self.start_menu.change_name = True
                                self.start_menu.join = False
                                
                            elif name == 'Quit' :
                                pygame.QUIT
                                sys.exit()
                                
                    if self.start_menu.join:
                        for name, rect, host, port , curr_player in self.start_menu.join_buttons:
                            if rect.collidepoint(mouse_pos) and curr_player < 12:
                                self.start_menu.addr = (host, port)
                                self.main_menu_running = False
                                
                if self.start_menu.change_name:
                    self.start_menu.name_input.handle_event(event)                
                    if event.type == MOUSEBUTTONDOWN and self.start_menu.sm_button.collidepoint(mouse_pos):
                        change_name_done()
                if self.start_menu.create:
                    self.start_menu.server_name_input.handle_event(event)                
                    if event.type == MOUSEBUTTONDOWN and self.start_menu.sm_button.collidepoint(mouse_pos):
                        create_done()
                        
            self.start_menu.draw()
            pygame.display.update()
            self.clock.tick(FPS)  
        
    def run_intro(self):
        running = True
        self.intro = Intro()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    running = False
                        
            pygame.display.update()
            self.clock.tick(FPS)  
            self.intro.draw()
        

    def run(self):
        self.run_intro()
        while True:
            self.main_menu()
            (host, port) = self.start_menu.addr
            self.network.join_server(HOST, port)
            self.start_game()
    
    def start_game(self):
        disconnected = False
        while not disconnected:
            self.events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            for event in self.events:
                if event.type == pygame.QUIT:
                    if self.game_client:
                        self.game_client.network.shut_down(self.game_client.local_player.id)
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not self.select_menu.main_active:  
                    self.pause_menu.toggle()
                if not self.pause_menu.active:
                    self.select_menu.handle_event(event)

                if event.type == MOUSEBUTTONDOWN and self.pause_menu.active:
                    if self.pause_menu.disconnect_rect.collidepoint(mouse_pos):
                        self.network.disconect_to_current_server()
                        del self.game_client
                        self.game_client = None
                        self.pause_menu.toggle()
                        self.select_menu.buttons = self.select_menu.main_buttons
                        self.select_menu.toggle()
                        disconnected = True
                        
                    if self.pause_menu.cancel_rect.collidepoint(mouse_pos):
                        self.pause_menu.toggle()
            
                        
            if disconnected:
                return           
            
             
            if self.select_menu.val not in ["", "t", "ct"]:
                if not self.game_client:
                    self.game_client = GameClient(self.start_menu.default_name, self.select_menu.val, self.network)
                else:
                    self.network.change_team_request(self.game_client.local_player.id, self.select_menu.val)    
                    self.game_client.local_player.switch_team(self.select_menu.val)
                self.select_menu.val = ""
            
            
                    
            if self.game_client:
                self.screen.fill((255,255,255))
                self.game_client.event_handle(self.events)    
                self.game_client.run()
                self.game_client.pointer_rect.center = pygame.mouse.get_pos()
                self.screen.blit(self.game_client.pointer_image, self.game_client.pointer_rect)
            else:
                self.screen.fill((190,158,108))
                
            self.select_menu.draw()
            self.pause_menu.draw()
            
            #show fps
            fps = self.clock.get_fps()
            fps_text_render = self.font.render(f'FPS : {str(int(fps))}', False, (255,232,80))
            self.screen.blit(fps_text_render, (20, 20))
            
            
            pygame.display.update()
            self.clock.tick(FPS)                       