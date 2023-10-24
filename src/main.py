import pygame as pg
import game_page
import controller
import fighter
import json

def main():
    pg.init()
    pg.display.set_mode((1024, 512))


    with open('res/test.json') as f:
        fighter_propertie = json.load(f)
    fighter0 = fighter.fighter(fighter_propertie)
    fighter1 = fighter.fighter(fighter_propertie)
    fighter2 = fighter.fighter(fighter_propertie)
    fighter3 = fighter.fighter(fighter_propertie)
    controller0 = controller.controller()
    controller0.add_fighter(fighter0, 0, 0)
    controller0.add_fighter(fighter2, 0, 0)
    controller0.add_fighter(fighter3, 0, 2)
    controller0.add_fighter(fighter1, 1, 0)
    page0 = game_page.page()
    page0.controller = controller0

    page0.start()

if __name__ == '__main__':
    main()