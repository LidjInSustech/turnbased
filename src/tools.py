import pygame as pg
import pygame.freetype as ft

def get_font(size):
    return ft.SysFont(ft.get_default_font(), size)

def get_image(name, size = None):
    try:
        image = pg.image.load(f'res/{name}.png')
    except:
        image = pg.image.load('res/img.png')
    if size:
        return pg.transform.smoothscale(image.convert(), size)
    else:
        return image.convert()

def get_image_alpha(name, size = None):
    try:
        image = pg.image.load(f'res/{name}.png')
    except:
        image = pg.image.load('res/img.png')
    if size:
        return pg.transform.smoothscale(image.convert_alpha(), size)
    else:
        return image.convert_alpha()