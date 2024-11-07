from csv import reader
import pygame

def import_csv_layout(file_path, tiles_index = []):
    terain_map = []
    with open(file_path) as level_map:
        layout = reader(level_map, delimiter=",")
        for row in layout:
            if tiles_index == []:
                terain_map.append(list(row))
                continue
            filltered_row = []
            for tile in row:
                if int(tile) in tiles_index:
                    filltered_row.append(int(tile))
                else:
                    filltered_row.append(-1)
            terain_map.append(filltered_row)
                    
    return terain_map

def get_tile_texture(file_path, texture_index, tile_size):
    img = pygame.image.load(file_path).convert_alpha()
    # img.set_colorkey((0,0,0))
    
    img_width, img_height = img.get_size()
    tiles_per_row = img_width // tile_size
    tiles_per_col = img_height // tile_size
    
    x_index = texture_index % tiles_per_row
    y_index = texture_index // tiles_per_row
    
    tile_rect = pygame.Rect(x_index * tile_size, y_index * tile_size, tile_size, tile_size)
    
    tile_texture = img.subsurface(tile_rect)
    return tile_texture.convert_alpha()

def get_animation_from_img(file_path, animation_size, color_key):
    img = pygame.image.load(file_path).convert_alpha()
    img.set_colorkey(color_key)
    img_width, img_height = img.get_size()
    animations_per_row = img_width // animation_size
    animations_per_col = img_height // animation_size
    animations_list = []
    for x_index in range(animations_per_row):
        for y_index in range(animations_per_col):
            animation_rect = pygame.Rect(x_index * animation_size, y_index * animation_size, animation_size, animation_size)
            animations_list.append(img.subsurface(animation_rect))
    return animations_list

def get_sprite_from_sheet(sprite_sheet , size, index):
    img_width, img_height = sprite_sheet.get_size()
    tiles_per_row = img_width // size
    tiles_per_col = img_height // size
    
    x_index = index % tiles_per_row
    y_index = index // tiles_per_row
    
    tile_rect = pygame.Rect(x_index * size, y_index * size, size, size)
    
    tile_texture = sprite_sheet.subsurface(tile_rect)
    return tile_texture.convert_alpha()