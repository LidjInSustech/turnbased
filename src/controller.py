import pygame as pg

class ctrler:
    def __init__(self):
        self.fields = [[[]*3]*2]
        self.rect = pg.display.get_surface().get_rect()
        self.create_background()
        self.explain = None
        self.actived = None
        self.pressed = None

    def add_fighter(self, fighter, faction, field):
        self.fields[faction][field].append(fighter)

    def create_field_rects(self):
        rect = self.rect
        self.field_rects = [[],[]]
        # x_range from 0.02 to 0.44, move 0.14, magin 0.02
        rect0 = pg.Rect(rect.w*0.02, rect.h*0.1, rect.w*0.12, rect.h*0.62)
        for i in range(3):
            surface = self.rect_inactive(rect0)
            self.field_rects[0].append((surface, rect0))
            rect0 = rect0.move(rect.w*0.14, 0)
        # x_range from 0.56 to 0.98, move 0.14, magin 0.02
        rect1 = pg.Rect(rect.w*0.56, rect.h*0.1, rect.w*0.12, rect.h*0.62)
        for i in range(3):
            surface = self.rect_inactive(rect1)
            self.field_rects[1].append((surface, rect1))
            rect1 = rect1.move(rect.w*0.14, 0)

    def create_button_rects(self):
        rect = self.rect
        self.buttons = [[],[]]
        # y_range from 0.74 to 0.85
        # x_range from 0.02 to 0.98, magin 0.02, move 0.32
        rect0 = pg.Rect(rect.w*0.02, rect.h*0.74, rect.w*0.3, rect.h*0.11)
        for i in range(3):
            surface = self.rect_inactive(rect0)
            self.buttons[0].append((surface, rect0))
            rect0 = rect0.move(rect.w*0.32, 0)
        # y_range from 0.87 to 0.98
        # x_range from 0.02 to 0.98, magin 0.02, move 0.32
        rect1 = pg.Rect(rect.w*0.02, rect.h*0.87, rect.w*0.3, rect.h*0.11)
        for i in range(3):
            surface = self.rect_inactive(rect1)
            self.buttons[1].append((surface, rect1))
            rect1 = rect1.move(rect.w*0.32, 0)

    def create_background(self):
        self.create_field_rects()
        self.create_button_rects()
        surface = pg.Surface(self.rect.size)
        surface.fill((0,0,0))
        for i in range(2):
            for j in range(3):
                surface.blit(self.field_rects[i][j][0], self.field_rects[i][j][1])
                surface.blit(self.buttons[i][j][0], self.buttons[i][j][1])
        self.background = surface

    def draw(self):
        pg.display.get_surface().blit(self.background, self.rect)
        if self.explain:
            pg.display.get_surface().blit(self.explain[0], self.explain[1])
        if self.actived:
            pg.display.get_surface().blit(self.rect_active(self.actived[1]), self.actived[1])
        if self.pressed:
            pg.display.get_surface().blit(self.rect_pressed(self.pressed[1]), self.pressed[1])

    def set_active(self, pos):
        if self.actived:
            self.actived = self.rect_inactive(self.actived[1])
            self.actived = None
        self.explain = None
        for i in range(3):
            if self.field_rects[0][i][1].collidepoint(pos):
                self.actived = self.field_rects[0][i]
                rect = self.field_rects[0][i][1].move(self.rect.w*0.12, 0)
                rect.size = (self.rect.w*0.28, self.rect.h*0.59)
                surface = self.rect_explain(rect)
                self.explain = (surface, rect)
                return
            
        for i in range(3):
            if self.field_rects[1][i][1].collidepoint(pos):
                self.actived = self.field_rects[1][i]
                rect = self.field_rects[1][i][1].move(-self.rect.w*0.28, 0)
                rect.size = (self.rect.w*0.28, self.rect.h*0.59)
                surface = self.rect_explain(rect)
                self.explain = (surface, rect)
                return
        
        for j in range(2):
            for i in range(3):
                if self.buttons[j][i][1].collidepoint(pos):
                    self.actived = self.buttons[j][i]
                    rect = self.buttons[j][i][1].move(0, -self.rect.h*0.3)
                    rect.size = (self.rect.w*0.3, self.rect.h*0.3)
                    surface = self.rect_explain(rect)
                    self.explain = (surface, rect)
                    return
                
    def set_pressed(self, pos):
        for j in range(2):
            for i in range(3):
                if self.buttons[j][i][1].collidepoint(pos):
                    self.pressed = self.buttons[j][i]
                    return
                
    def start(self):
        clock = pg.time.Clock()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                if event.type == pg.MOUSEMOTION:
                    self.set_active(event.pos)
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.set_pressed(event.pos)
            self.draw()
            pg.display.update()
            clock.tick(60)

    def rect_explain(self, rect):
        surface = pg.Surface(rect.size)
        surface.fill((255,255,255))
        surface.set_alpha(128)
        return surface
    
    def rect_inactive(self, rect):
        surface = pg.Surface(rect.size)
        surface.fill((0,0,0))
        surface.set_colorkey((0,0,0))
        pg.draw.rect(surface, (255,255,255), surface.get_rect(), 3)
        return surface
    
    def rect_active(self, rect):
        surface = pg.Surface(rect.size, pg.SRCALPHA)
        pg.draw.rect(surface, (255,255,255,128), surface.get_rect())
        pg.draw.rect(surface, (255,255,255,255), surface.get_rect(), 3)
        return surface
    
    def rect_pressed(self, rect):
        surface = pg.Surface(rect.size, pg.SRCALPHA)
        #pg.draw.rect(surface, (255,255,255,128), surface.get_rect())
        pg.draw.rect(surface, (255,0,0,255), surface.get_rect(), 3)
        return surface