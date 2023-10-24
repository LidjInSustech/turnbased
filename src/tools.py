import pygame as pg
import pygame.freetype as ft

def get_font(size):
    return ft.SysFont(ft.get_default_font(), size)

def get_image(path, size = None):
    if size:
        surface = pg.Surface(size)
        surface.fill((255,255,255))
        return surface

def get_image_(path, size = None):
    if size:
        return pg.transform.smoothscale(pg.image.load(path).convert(), size)
    else:
        return pg.image.load(path).convert()

def get_image_alpha(path, size = None):
    if size:
        return pg.transform.smoothscale(pg.image.load(path).convert_alpha(), size)
    else:
        return pg.image.load(path).convert_alpha()