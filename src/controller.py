import pygame as pg

class controller:
    def __init__(self):
        self.fields = [[[],[],[]],[[],[],[]]]
        self.all_fighters = pg.sprite.Group()
        self.time = 0
        self.prepared_fighter = []

    def add_fighter(self, fighter, faction, field):
        fighter.faction = faction
        fighter.field = field
        self.fields[faction][field].append(fighter)
        self.all_fighters.add(fighter)

    def tick(self):
        self.time += 1
        for i in self.all_fighters:
            if i.tick():
                self.prepared_fighter.append(i)
            
    def start(self):
        while len(self.prepared_fighter) < 1:
            self.tick()
        self.prepared_fighter.sort(key=lambda x: x.ap, reverse=True)

    # actions

    def skip(self):
        while self.prepared_fighter[0].ap >= 5:
            self.prepared_fighter[0].ap -= 1
            self.prepared_fighter.pop(0)
            return True
        
    def move(self, destination):
        if self.prepared_fighter[0].ap >= 2:
            self.prepared_fighter[0].ap -= 2
            self.fields[self.prepared_fighter[0].faction][self.prepared_fighter[0].field].remove(self.prepared_fighter[0])
            self.prepared_fighter[0].field = destination
            self.fields[self.prepared_fighter[0].faction][self.prepared_fighter[0].field].append(self.prepared_fighter[0])
            return True
        return False
        
    def cast(self, spell, target_field, target_fighter):
        return True
            