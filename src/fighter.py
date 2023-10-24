import pygame as pg
import tools

class fighter(pg.sprite.Sprite):
    def __init__(self, properties):
        super().__init__()
        self.initial = properties
        self.current = self.initial.copy()
        self.hp = self.current['maxhp']
        self.mp = self.current['maxmp']
        self.ap = self.current['maxap']
        self.effects = []

        width = pg.display.get_surface().get_width()*0.1
        self.rect = pg.Rect(0, 0, width, width)
        self.inactive_image = tools.get_image(self.initial['name'], self.rect.size)
        self.active_image = self.inactive_image.copy()
        pg.draw.rect(self.active_image, (255,255,255), self.rect, 3)
        pg.draw.rect(self.inactive_image, (128,128,128), self.rect, 3)
        self.image = self.inactive_image.copy()
        self.state = 'inactive'

    @property
    def i(self):
        return self.initial
    
    @property
    def c(self):
        return self.current
    
    def tick(self):
        self.mp += self.c['mpregen']
        self.ap += self.c['speed']
        for i in self.effects:
            i.tick()
        if self.ap >= self.c['maxap']:
            return True
        return False
    
    def inactivate(self):
        self.image = self.inactive_image.copy()
        self.state = 'inactive'

    def activate(self):
        self.image = self.active_image.copy()
        self.state = 'active'