import pygame as pg
import tools
import math
import datetime

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
        self.origin_image = tools.get_image('fighters_image/'+self.initial['name'], self.rect.size)
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
    
    def damage(self, type, value):
        value *= math.pow(0.5, self.c['resist'][type]/100)
        self.hp -= value
    
    def tick(self):
        self.current = self.initial.copy()
        for i in range(len(self.effects)-1, -1, -1):
            self.effect_action(i)

        if self.hp > self.c['maxhp']:
            self.hp = self.c['maxhp']
        self.mp += self.c['mpregen']
        if self.mp > self.c['maxmp']:
            self.mp = self.c['maxmp']
        self.ap += self.c['speed']
        if self.ap >= self.c['maxap']:
            return True
        return False
    
    def effect_action(self, i):
        effect = self.effects[i]
        for k, v in effect['values'].items():
            if k in self.c:
                self.c[k] += v
            elif k in self.c['resist']:
                self.c['resist'][k] += v
            elif k == 'hp':
                self.hp += v
            elif k == 'mp':
                self.mp += v
            elif k == 'ap':
                self.ap += v
            else:
                raise Exception(f"Unknown effect value {k}")
        if 'duration' in effect:
            effect['duration'] -= 1
            if effect['duration'] <= 0:
                self.effects.pop(i)

    def update(self):
        image = self.origin_image.copy()
        if self.actioning:
            color = datetime.datetime.now().microsecond / 2000 % 255
            pg.draw.rect(image, (color,0,255-color), self.ori_rect, 3)
        elif self.prepared:
            pg.draw.rect(image, (0,255,0), self.ori_rect, 3)
        elif self.actived:
            pg.draw.rect(image, (255,255,255), self.ori_rect, 3)
        else:
            pg.draw.rect(image, (128,128,128), self.ori_rect, 3)
        self.image = image

    def info(self):
        return [self.i['name'], 
                f"{self.hp:4.1f}/{self.c['maxhp']:4.1f}",
                f"{self.mp:4.1f}/{self.c['maxmp']:4.1f}",
                f"{self.ap}/{self.c['maxap']:4.1f}"]

    def rect_explain(self, rect, font):
        surface = pg.Surface(rect.size)
        surface.fill((255,255,255))
        surface.set_alpha(128)
        begin = self.draw_basic(surface, font, (0,0))
        self.draw_effect(surface, font, begin)
        return surface
    
    def draw_basic(self, surface, font, begin):
        length = surface.get_width()
        title = ['HP', 'MP', 'AP']
        colors = [(255,0,0), (0,0,255), (255,255,0)]
        values = [self.hp, self.mp, self.ap]
        maxvalues = [self.c['maxhp'], self.c['maxmp'], self.c['maxap']]
        info = self.info()
        text, text_rect = font.render(f"{self.i['name']}", (0,0,0))
        surface.blit(text, begin)
        begin = (begin[0], begin[1]+font.size)
        for i in range(len(info)-1):
            text, text_rect = font.render(f"{title[i]:6}{info[i+1]}", (0,0,0))
            pg.draw.rect(surface, colors[i], (begin[0], begin[1], length*values[i]/maxvalues[i], font.size))
            surface.blit(text, begin)
            begin = (begin[0], begin[1]+font.size)
        return begin
    
    def draw_effect(self, surface, font, begin):
        for i in range(len(self.effects)):
            effect = self.effects[i]
            text, text_rect = font.render(f"{effect['name']}: {effect['duration']}", (0,0,0))
            surface.blit(text, begin)
            begin = (begin[0], begin[1]+font.size)
        return begin