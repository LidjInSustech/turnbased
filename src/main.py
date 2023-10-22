import pygame as pg
import controller

def main():
    pg.init()
    pg.display.set_mode((1024, 512))
    controller.ctrler().start()

if __name__ == '__main__':
    main()