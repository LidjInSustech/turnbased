import pygame as pg
import tools

class fighter(pg.sprite.Sprite):
    def __init__(self, properties):
        super().__init__()
        self.initial = properties
        self.current = self.initial.copy()
        self.hp = self.current['maxhp']
        self.mp = self.current['maxmp']
        self.ap = 0
        self.effects = []

        width = pg.display.get_surface().get_width()*0.1
        self.ori_rect = pg.Rect(0, 0, width, width)
        self.rect = self.ori_rect.copy()
        self.origin_image = tools.get_image(self.initial['name'], self.rect.size)
        self.image = self.origin_image.copy()
        pg.draw.rect(self.image, (128,128,128), self.rect, 3)
        self.actived = False
        self.prepared = False
        self.actioning = False

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
    
    def update(self):
        image = self.origin_image.copy()
        if self.actioning:
            pg.draw.rect(image, (255,255,0), self.ori_rect, 3)
        elif self.prepared:
            pg.draw.rect(image, (0,255,0), self.ori_rect, 3)
        elif self.actived:
            pg.draw.rect(image, (255,255,255), self.ori_rect, 3)
        else:
            pg.draw.rect(image, (128,128,128), self.ori_rect, 3)
        self.image = image

    def info(self):
        return [self.i['name'], 
                f"{self.hp}/{self.c['maxhp']}",
                f"{self.mp}/{self.c['maxmp']}",
                f"{self.ap}/{self.c['maxap']}"]

    def rect_explain(self, rect, font):
        title = ['name', 'hp', 'mp', 'ap']
        surface = pg.Surface(rect.size)
        surface.fill((255,255,255))
        surface.set_alpha(128)
        for i in range(len(title)):
            text, text_rect = font.render(f"{title[i]}: {self.info()[i]}", (0,0,0))
            surface.blit(text, (0, i*font.size))
        return surface