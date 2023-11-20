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
        self.mid_font = tools.get_font(int(self.rect.h*0.06))
        self.small_font = tools.get_font(int(self.rect.h*0.04))

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
            button_ = button(rect0, message, self.mid_font)
            self.buttons.add(button_)
            rect0 = rect0.move(rect.w*0.32, 0)
        # y_range from 0.87 to 0.98
        # x_range from 0.02 to 0.98, magin 0.02, move 0.32
        rect1 = pg.Rect(rect.w*0.02, rect.h*0.87, rect.w*0.3, rect.h*0.11)
        for message in ['move', 3, 4]:
            button_ = button(rect1, message, self.mid_font)
            self.buttons.add(button_)
            rect1 = rect1.move(rect.w*0.32, 0)

        self.skills_buttons = list()
        for i in self.buttons:
            if i.message in (1,2,3,4):
                self.skills_buttons.append(i)
            if i.message == 'skip':
                i.load_description('skip the turn')
            elif i.message == 'move':
                i.load_description('move to the field')

    def create_background(self):
        surface = pg.Surface(self.rect.size)
        surface.fill((0,0,0))
        self.background = surface

    def draw(self):
        surface = self.background.copy()
        self.fields.update()
        self.buttons.update()
        self.fields.draw(surface)
        self.buttons.draw(surface)
        self.draw_fighters(surface)
        if self.explain:
            surface.blit(self.explain[0], self.explain[1])
        self.mid_font.render_to(surface, (0,0), ' time: '+str(self.controller.time), (255,255,255))
        self.last_surface = surface
        pg.display.get_surface().blit(surface, (0,0))

    def draw_fighters(self, surface):
        self.controller.all_fighters.update()
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
            i.actived = False
        for i in self.fields:
            i.actived = False
        for i in self.controller.all_fighters:
            if i.actived == True:
                i.actived = False
                i.update()
        self.actived = None
        self.explain = None
        
        for i in self.fields:
            if i.rect.collidepoint(pos):
                i.actived = True
                self.actived = i

        for i in self.buttons:
            if i.rect.collidepoint(pos):
                if i.actived == False:
                    i.actived = True
                    self.actived = i
                rect = i.rect.move(0, -self.rect.h*0.3)
                rect.size = (self.rect.w*0.3, self.rect.h*0.3)
                surface = i.rect_explain(rect, self.small_font)
                if surface:
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
                surface = i.rect_explain(rect, self.small_font)
                self.explain = (surface, rect)
                
    def set_pressed(self, pos):
        for i in self.buttons:
            if i.rect.collidepoint(pos):
                if self.pressed is not None:
                    self.pressed.pressed = False
                    if self.pressed == i:
                        self.pressed = None
                        return
                if i.message == 'skip':
                    self.controller.skip()
                    return
                i.pressed = True
                self.pressed = i
                return
            
        if self.pressed is None:
            return
        faction, field, fighter = self.get_target(pos)
        if self.pressed.message == 'move':
            if self.controller.move(faction, field):
                self.pressed.pressed = False
                self.pressed = None
        else:
            if self.controller.cast(self.pressed.message, faction, field, fighter):
                self.pressed.pressed = False
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
        for f in self.controller.all_fighters:
            if f.rect.collidepoint(pos):
                fighter = f
        return faction, field, fighter

    def load_controller(self, controller):
        self.controller = controller

    def load_skills(self):
        skills = self.controller.prepared_fighter[0].c['skills']
        for i, skill in enumerate(skills):
            self.skills_buttons[i].message = skill['name']
            self.skills_buttons[i].load_description(skill['description'])
            self.skills_buttons[i].icon_rect = pg.Rect(self.rect.h*0.01, self.rect.h*0.01, self.rect.h*0.09, self.rect.h*0.09)
            self.skills_buttons[i].icon = tools.get_image(skill['name'], (self.rect.h*0.09, self.rect.h*0.09))
        for i in range(len(skills), 4):
            self.skills_buttons[i].message = ''
            self.skills_buttons[i].load_description(None)
            self.skills_buttons[i].icon = None

    def animation(self, clock):
        while len(self.controller.events) > 0:
            event = self.controller.events.pop(0)
            match event['type']:
                case 'move':
                    self.move_animation(event, clock)
                case 'cast':
                    self.cast_animation(event, clock)

    def move_animation(self, event, clock):
        rect = self.rect
        if event['faction'] == 0:
            from_pos = (rect.w*(0.31-0.14*event['from'][0]) , 
                        rect.h*0.1 + (self.rect.h*0.52*(0.5+event['from'][1]))/(len(self.controller.fields[0][event['from'][0]])+1) - rect.h*0.05)
            to_pos = (rect.w*(0.31-0.14*event['to']) ,
                        rect.h*0.1 + (self.rect.h*0.52*(len(self.controller.fields[0][event['to']])-0.5))/len(self.controller.fields[0][event['to']]) - rect.h*0.05)
        else:
            from_pos = (rect.w*(0.57+0.14*event['from'][0]) ,
                        rect.h*0.1 + (self.rect.h*0.52*(0.5+event['from'][1]))/(len(self.controller.fields[1][event['from'][0]])+1) - rect.h*0.05)
            to_pos = (rect.w*(0.57+0.14*event['to']) ,
                        rect.h*0.1 + (self.rect.h*0.52*(len(self.controller.fields[1][event['to']])-0.5))/len(self.controller.fields[1][event['to']]) - rect.h*0.05)

        frames = 15
        for i in range(frames):
            surface = self.last_surface.copy()
            fighter = event['fighter']
            frect = fighter.rect.copy()
            frect.topleft = (from_pos[0] + (to_pos[0]-from_pos[0])*i/frames, from_pos[1] + (to_pos[1]-from_pos[1])*i/frames)
            surface.blit(fighter.image, frect)
            pg.display.get_surface().blit(surface, (0,0))
            pg.display.update()
            clock.tick(60)

    def cast_animation(self, event, clock):
        rect = self.rect
        from_pos = self.get_pos(*event['from'])
        to_pos = self.get_pos(*event['to'])
        bullet = tools.get_image_alpha('bullet', (int(rect.w*0.03), int(rect.w*0.03)))
        brect = bullet.get_rect()

        frames = 15
        for i in range(frames):
            surface = self.last_surface.copy()
            brect.center = (from_pos[0] + (to_pos[0]-from_pos[0])*i/frames, from_pos[1] + (to_pos[1]-from_pos[1])*i/frames)
            surface.blit(bullet, brect)
            pg.display.get_surface().blit(surface, (0,0))
            pg.display.update()
            clock.tick(60)

    def get_pos(self, faction, field, index, length):
        rect = self.rect
        if faction == 0:
            pos = (rect.w*(0.36-0.14*field) ,
                   rect.h*0.1 + (self.rect.h*0.52*(0.5+index))/(length) - rect.h*0.05 + rect.w*0.05)
        else:
            pos = (rect.w*(0.62+0.14*field) ,
                   rect.h*0.1 + (self.rect.h*0.52*(0.5+index))/(length) - rect.h*0.05 + rect.w*0.05)
        return pos

    def start(self):
        self.available = True
        self.create_field_rects()
        self.create_button_rects()
        clock = pg.time.Clock()
        while self.controller.not_end():
            if len(self.controller.prepared_fighter) < 1:
                self.controller.start()
            self.load_skills()
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
            self.animation(clock)
    
class button(pg.sprite.Sprite):
    def __init__(self, rect, message = '', font = None):
        super().__init__()
        self.message = message
        self.font = font

        self.rect = rect
        self.ori_rect = self.rect.copy()
        self.ori_rect.topleft = (0,0)
        self.origin_image = pg.Surface(rect.size)
        self.origin_image.fill((0,0,0))
        self.origin_image.set_colorkey((0,0,0))
        self.image = self.origin_image.copy()
        pg.draw.rect(self.image, (128,128,128), self.image.get_rect(), 3)

        self.actived = False
        self.pressed = False

        self.icon_rect = None
        self.icon = None

    def update(self):
        if self.pressed:
            self.image = self.origin_image.copy()
            pg.draw.rect(self.image, (255,255,0), self.image.get_rect(), 3)
        elif self.actived:
            self.image = self.origin_image.copy()
            pg.draw.rect(self.image, (255,255,255), self.image.get_rect(), 3)
        else:
            self.image = self.origin_image.copy()
            pg.draw.rect(self.image, (128,128,128), self.image.get_rect(), 3)

        # render icon
        if self.icon:
            self.image.blit(self.icon, self.icon_rect)
            
        # render message
        if self.font:
            text, text_rect = self.font.render(str(self.message),  fgcolor=(255,255,255))
            text_rect.center = self.ori_rect.center
            if self.icon_rect:
                text_rect.move_ip(self.icon_rect.w/2, 0)
            self.image.blit(text, text_rect)

    def load_description(self, description):
        if description is None:
            self.descriptions = None
            return
        
        row_width = 20
        self.descriptions = list()
        for i in range(len(description)//row_width):
            self.descriptions.append(description[i*row_width:(i+1)*row_width])
        self.descriptions.append(description[(len(description)//row_width)*row_width:])
        
    def rect_explain(self, rect, font):
        if self.descriptions is None:
            return None
        surface = pg.Surface(rect.size)
        surface.fill((255,255,255))
        surface.set_alpha(128)
        for i in range(len(self.descriptions)):
            text, text_rect = font.render(self.descriptions[i], (0,0,0))
            text_rect.topleft = (0, i*font.size)
            surface.blit(text, text_rect)
        return surface
