import pygame as pg
import controller

def main():
    pg.init()
    screen = pg.display.set_mode((1024, 768))
    controller.ctrler().start()

if __name__ == '__main__':
    main()