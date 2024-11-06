# import pygame
# import sys

# # Khởi tạo Pygame
# pygame.init()

# # Thiết lập kích thước màn hình
# screen_width = 800
# screen_height = 600
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption("Giao Diện Pygame")

# # Định nghĩa màu sắc
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# YELLOW = (255, 255, 0)
# DARK_BLUE = (10, 10, 50)

# # Tạo hàm để vẽ văn bản
# def draw_text(text, font, color, surface, x, y):
#     text_obj = font.render(text, True, color)
#     text_rect = text_obj.get_rect()
#     text_rect.topleft = (x, y)
#     surface.blit(text_obj, text_rect)

# # Vòng lặp chính
# running = True
# font = pygame.font.SysFont("Arial", 30)
# while running:
#     screen.fill(DARK_BLUE)  # Đặt nền tối màu xanh đậm

#     # Vẽ thanh màu vàng trên cùng
#     pygame.draw.rect(screen, YELLOW, (0, 0, screen_width, 50))

#     # Vẽ tiêu đề
#     draw_text("Unreal Software's CS2D", font, WHITE, screen, 20, 60)

#     # Vẽ các tùy chọn menu
#     menu_options = [
#         "Quick Play", "New Game", "Find Servers",
#         "Options", "Friends", "Mods",
#         "Editor", "Help", "Discord", "Quit"
#     ]
#     y_offset = 120
#     for option in menu_options:
#         draw_text(option, font, WHITE, screen, 20, y_offset)
#         y_offset += 40

#     # Xử lý sự kiện
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Cập nhật màn hình
#     pygame.display.flip()

# # Thoát Pygame
# pygame.quit()
# sys.exit()
import pygame

class Intro:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.background = pygame.transform.scale(pygame.image.load('assets/intro/CS2D.png'), (1280, 720)).convert()
        self.background_rect = self.background.get_rect()

        
        self.font = pygame.font.Font('assets/fonts/UI_font.ttf', 30)  
        self.text_color = (0, 0, 0)
        self.text = self.font.render("Press anywhere to continue", True, self.text_color)
        self.text_rect = self.text.get_rect(center=(640, 560))

       
        self.alpha_surface = pygame.Surface((self.text_rect.width + 20, self.text_rect.height + 20))
        self.alpha_surface.set_alpha(128) 
        self.alpha_surface.fill((255, 255, 255))

        
        self.blink = True
        self.blink_interval = 0.4  
        self.last_blink_time = pygame.time.get_ticks() / 1000
        
        self.intro_menu_active = True

    def draw(self):
        if self.intro_menu_active :
            cur = pygame.time.get_ticks() / 1000
            if cur - self.last_blink_time >= self.blink_interval:
                self.blink = not self.blink
                self.last_blink_time = cur

            
            self.display_surface.blit(self.background, (0, 0))

            
            alpha_rect = self.alpha_surface.get_rect(center=self.text_rect.center)
            self.display_surface.blit(self.alpha_surface, alpha_rect)

        
            if self.blink:
                self.display_surface.blit(self.text, self.text_rect)
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.intro_menu_active:
            mouse_pos = pygame.mouse.get_pos()
            if self.background_rect.collidepoint(mouse_pos):
                self.intro_menu_active = False