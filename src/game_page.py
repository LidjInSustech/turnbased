import pygame as pg
import tools

class page:
    def __init__(self):
        self.controller = None
        self.rect = pg.display.get_surface().get_rect()
        self.create_background()
        self.explain = None
        self.actived = None
        self.pressed = None
        self.available = False
        self.small_font = tools.get_font(int(self.rect.h*0.06))

    def create_field_rects(self):
        rect = self.rect
        self.fields = pg.sprite.Group()
        # x_range from 0.02 to 0.44, move 0.14, magin 0.02
        rect0 = pg.Rect(rect.w*0.02, rect.h*0.1, rect.w*0.12, rect.h*0.62)
        for i in range(3):
            field = button(rect0, -3+i)
            self.fields.add(field)
            rect0 = rect0.move(rect.w*0.14, 0)
        # x_range from 0.56 to 0.98, move 0.14, magin 0.02
        rect1 = pg.Rect(rect.w*0.56, rect.h*0.1, rect.w*0.12, rect.h*0.62)
        for i in range(3):
            field = button(rect1, 1+i)
            self.fields.add(field)
            rect1 = rect1.move(rect.w*0.14, 0)

    def create_button_rects(self):
        rect = self.rect
        self.buttons = pg.sprite.Group()
        # y_range from 0.74 to 0.85
        # x_range from 0.02 to 0.98, magin 0.02, move 0.32
        rect0 = pg.Rect(rect.w*0.02, rect.h*0.74, rect.w*0.3, rect.h*0.11)
        for message in ['skip', 1, 2]:
            button_ = button(rect0, message)
            self.buttons.add(button_)
            rect0 = rect0.move(rect.w*0.32, 0)
        # y_range from 0.87 to 0.98
        # x_range from 0.02 to 0.98, magin 0.02, move 0.32
        rect1 = pg.Rect(rect.w*0.02, rect.h*0.87, rect.w*0.3, rect.h*0.11)
        for message in ['move', 3, 4]:
            button_ = button(rect1, message)
            self.buttons.add(button_)
            rect1 = rect1.move(rect.w*0.32, 0)

    def create_background(self):
        surface = pg.Surface(self.rect.size)
        surface.fill((0,0,0))
        self.background = surface

    def draw(self):
        surface = self.background.copy()
        self.fields.draw(surface)
        self.buttons.draw(surface)
        self.draw_fighters(surface)
        if self.explain:
            surface.blit(self.explain[0], self.explain[1])
        self.small_font.render_to(surface, (0,0), ' time: '+str(self.controller.time), (255,255,255))
        pg.display.get_surface().blit(surface, (0,0))

    def draw_fighters(self, surface):
        rect = self.rect
        for i, field in enumerate(self.controller.fields[0]):
            num = len(field)
            if num > 0:
                height = self.rect.h*0.52/num
                pos = (rect.w*(0.31-0.14*i) , rect.h*0.1 + height/2 - rect.h*0.05)
                for fighter in field:
                    fighter.rect.topleft = pos
                    pos = (pos[0], pos[1]+height)
        for i, field in enumerate(self.controller.fields[1]):
            num = len(field)
            if num > 0:
                height = self.rect.h*0.52/num
                pos = (rect.w*(0.57+0.14*i) , rect.h*0.1 + height/2 - rect.h*0.05)
                for fighter in field:
                    fighter.rect.topleft = pos
                    pos = (pos[0], pos[1]+height)
        self.controller.all_fighters.draw(surface)
                    

    def set_active(self, pos):
        for i in self.buttons:
            i.inactivate()
        for i in self.fields:
            i.inactivate()
        for i in self.controller.all_fighters:
            if i.actived == True:
                i.actived = False
                i.update()
        self.actived = None
        self.explain = None
        
        for i in self.fields:
            if i.rect.collidepoint(pos):
                i.activate()
                self.actived = i

        for i in self.buttons:
            if i.rect.collidepoint(pos):
                if i.state == 'inactive':
                    i.activate()
                    self.actived = i
                rect = i.rect.move(0, -self.rect.h*0.3)
                rect.size = (self.rect.w*0.3, self.rect.h*0.3)
                surface = self.rect_explain(rect)
                self.explain = (surface, rect)

        for i in self.controller.all_fighters:
            if i.rect.collidepoint(pos):
                i.actived = True
                i.update()
                self.actived = i
                if i.rect.centerx < self.rect.w/2:
                    rect = i.rect.move(i.rect.w, 0)
                else:
                    rect = i.rect.move(-self.rect.w*0.2, 0)
                rect.size = (self.rect.w*0.2, self.rect.h*0.5)
                surface = self.rect_explain(rect)
                self.explain = (surface, rect)
                
    def set_pressed(self, pos):
        for i in self.buttons:
            if i.rect.collidepoint(pos):
                if self.pressed is not None:
                    self.pressed.activate()
                    if self.pressed == i:
                        self.pressed = None
                if i.message == 'skip':
                    self.controller.skip()
                    return
                i.press()
                self.pressed = i
                return
        
        faction, field, fighter = self.get_target(pos)
        if self.pressed.message == 'move':
            if self.controller.move(faction, field):
                self.pressed.activate()
                self.pressed = None
        elif self.pressed.message in (1,2,3,4):
            if self.controller.cast(self.pressed.message, faction, field, fighter):
                self.pressed.activate()
                self.pressed = None
        
            
    def get_target(self, pos):
        faction = None
        field = None
        fighter = None
        for i in self.fields:
            if i.rect.collidepoint(pos):
                if i.message < 0:
                    faction = 0
                else:
                    faction = 1
                field = abs(i.message) - 1
        for fighter in self.controller.all_fighters:
            if i.rect.collidepoint(pos):
                fighter = i
        return faction, field, fighter

    def load_controller(self, controller):
        self.controller = controller

    def start(self):
        self.available = True
        self.create_field_rects()
        self.create_button_rects()
        clock = pg.time.Clock()
        while True:
            if len(self.controller.prepared_fighter) < 1:
                self.controller.start()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                if self.available:
                    if event.type == pg.MOUSEBUTTONDOWN:
                        self.set_pressed(event.pos)
            if self.available:
                self.set_active(pg.mouse.get_pos())
            self.draw()
            pg.display.update()
            clock.tick(60)

    def rect_explain(self, rect):
        surface = pg.Surface(rect.size)
        surface.fill((255,255,255))
        surface.set_alpha(128)
        return surface
    
class button(pg.sprite.Sprite):
    def __init__(self, rect, message = ''):
        super().__init__()
        self.rect = rect
        # inactive
        surface = pg.Surface(rect.size)
        surface.fill((0,0,0))
        surface.set_colorkey((0,0,0))
        pg.draw.rect(surface, (128,128,128), surface.get_rect(), 3)
        self.inactive = surface
        # active
        surface = pg.Surface(rect.size)
        pg.draw.rect(surface, (255,255,255), surface.get_rect(), 3)
        self.active = surface
        # pressed
        surface = pg.Surface(rect.size)
        pg.draw.rect(surface, (255,255,0), surface.get_rect(), 3)
        self.pressed = surface
        self.image = self.inactive.copy()
        self.state = 'inactive'
        self.message = message

    def inactivate(self):
        if self.state == 'active':
            self.image = self.inactive.copy()
            self.state = 'inactive'

    def activate(self):
        self.image = self.active.copy()
        self.state = 'active'

    def press(self):
        self.image = self.pressed.copy()
        self.state = 'pressed'