import pygame as pg
import game_page
import controller
import fighter
import tools

def main():
    pg.init()
    pg.display.set_mode((1024, 512))

    fighter0 = fighter.fighter(tools.get_fighter('zao_nan'))
    fighter1 = fighter.fighter(tools.get_fighter('za_bing'))
    controller0 = controller.controller()
    controller0.add_fighter(fighter0, 0, 0)
    controller0.add_fighter(fighter1, 1, 0)
    page0 = game_page.page()
    page0.controller = controller0

    page0.start()

if __name__ == '__main__':
    main()