import pygame as pg
import pygame.freetype as ft
import json

def get_font(size):
    return ft.SysFont('Microsoft YaHei UI', size)

def get_image(name, size = None):
    try:
        image = pg.image.load(f'res/{name}.png')
    except:
        print(f'Error: res/{name}.png not found')
        image = pg.image.load('res/null.png')
    if size:
        return pg.transform.smoothscale(image.convert(), size)
    else:
        return image.convert()

def get_image_alpha(name, size = None):
    try:
        image = pg.image.load(f'res/{name}.png')
    except:
        print(f'Error: res/{name}.png not found')
        image = pg.image.load('res/null.png')
    if size:
        return pg.transform.smoothscale(image.convert_alpha(), size)
    else:
        return image.convert_alpha()
    
def get_fighter(name):
    try:
        with open(f'res/fighters_data/{name}.json', 'r', encoding='utf8') as f:
            fighter_propertie = json.load(f)
            return fighter_propertie
    except:
        with open('res/test.json', 'r', encoding='utf8') as f:
            fighter_propertie = json.load(f)
            return fighter_propertie