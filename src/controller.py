import pygame as pg
import auto

class controller:
    def __init__(self):
        self.fields = [[[],[],[]],[[],[],[]]]
        self.all_fighters = pg.sprite.Group()
        self.time = 0
        self.prepared_fighter = []
        self.events = []
        self.autonomous = [None, auto.auto(self)]

    def add_fighter(self, fighter, faction, field):
        fighter.faction = faction
        fighter.field = field
        self.fields[faction][field].append(fighter)
        self.all_fighters.add(fighter)

    def remove_fighter(self, fighter):
        self.fields[fighter.faction][fighter.field].remove(fighter)
        self.all_fighters.remove(fighter)

    def not_end(self):
        for i in self.all_fighters:
            if i.hp <= 0:
                self.remove_fighter(i)
        len1 =  len(self.fields[0][0])+len(self.fields[0][1])+len(self.fields[0][2])
        len2 =  len(self.fields[1][0])+len(self.fields[1][1])+len(self.fields[1][2])
        return len1 > 0 and len2 > 0

    def tick(self):
        self.time += 1
        for i in self.all_fighters:
            if i.tick():
                self.prepared_fighter.append(i)
            
    def start(self):
        while len(self.prepared_fighter) < 1 or (self.autonomous[self.prepared_fighter[0].faction] is not None):
            while len(self.prepared_fighter) < 1:
                self.tick()
            self.prepared_fighter.sort(key=lambda x: x.ap, reverse=True)
            while len(self.prepared_fighter) > 0 and (self.autonomous[self.prepared_fighter[0].faction] is not None):
                self.autonomous[self.prepared_fighter[0].faction].next()
        
        #self.prepared_fighter.sort(key=lambda x: x.ap, reverse=True)
        for i in self.prepared_fighter:
            i.prepared = True
        self.prepared_fighter[0].actioning = True
        #self.all_fighters.update()

    # actions

    def skip(self):
        while self.prepared_fighter[0].ap >= 5:
            self.prepared_fighter[0].ap -= 1
        self.prepared_fighter[0].prepared = False
        self.prepared_fighter[0].actioning = False
        self.prepared_fighter[0].update()
        self.prepared_fighter.pop(0)
        if len(self.prepared_fighter) > 0:
            self.prepared_fighter[0].actioning = True
            self.prepared_fighter[0].update()
        return True
        
    def move(self, faction, destination):
        if faction != self.prepared_fighter[0].faction:
            return False
        if destination == self.prepared_fighter[0].field:
            return False
        if self.prepared_fighter[0].ap >= 2:
            # add animation
            self.events.append({'type': 'move', 'fighter': self.prepared_fighter[0], 'faction': faction, 
                                'from': (self.prepared_fighter[0].field, self.fields[self.prepared_fighter[0].faction][self.prepared_fighter[0].field].index(self.prepared_fighter[0])), 
                                'to': destination})
            # end animation
            
            self.prepared_fighter[0].ap -= 2
            self.fields[self.prepared_fighter[0].faction][self.prepared_fighter[0].field].remove(self.prepared_fighter[0])
            self.prepared_fighter[0].field = destination
            self.fields[self.prepared_fighter[0].faction][self.prepared_fighter[0].field].append(self.prepared_fighter[0])
            return True
        return False
        
    def cast(self, spell, target_faction, target_field, target_fighter):
        action_fighter = self.prepared_fighter[0]
        skills = action_fighter.c['skills']
        for i in skills:
            if i['name'] == spell:
                # check if the spell is valid
                if self.prepared_fighter[0].ap < i['cost']['ap']:
                    return False
                if self.prepared_fighter[0].mp < i['cost']['mp']:
                    return False
                
                requirements = i['requirements']
                if requirements['faction'] != 'any':
                    val = {'ally': 0, 'enemy': 1}
                    if (target_faction + action_fighter.faction) % 2 != val[requirements['faction']]:
                        return False
                    
                if target_field is None and requirements['field'] is not False:
                    return False
                if target_fighter is None and requirements['fighter'] is not False:
                    return False
                # scuessful cast
                self.prepared_fighter[0].ap -= i['cost']['ap']
                self.prepared_fighter[0].mp -= i['cost']['mp']
                # action
                for action in i['actions']:
                    match action['type']:
                        case 'damage':
                            value = action['value']
                            atk = action_fighter.c['atk']/100.
                            if action['target'] == 'target_fighter':
                                for k, v in value.items():
                                    target_fighter.damage(k, v * atk)
                            #if target_fighter.hp <= 0:
                            #    self.remove_fighter(target_fighter)

                            #print(action_fighter.c['name'], 'use skill', i['name'], 'to', target_fighter.c['name'], 'damage', value, 'atk', atk)
                            self.events.append({'type': 'cast', 
                                    'from': (action_fighter.faction, action_fighter.field, self.fields[action_fighter.faction][action_fighter.field].index(action_fighter), len(self.fields[action_fighter.faction][action_fighter.field])),
                                    'to': (target_faction, target_field, self.fields[target_faction][target_field].index(target_fighter), len(self.fields[target_faction][target_field])),
                                    'bullet_img': action['bullet_img'], 'demage_img': action['demage_img'], 'value': value})
                        case _:
                            return False
                self.events.append({'type': 'cast', 
                                    'from': (action_fighter.faction, action_fighter.field, self.fields[action_fighter.faction][action_fighter.field].index(action_fighter), len(self.fields[action_fighter.faction][action_fighter.field])),
                                    'to': (target_faction, target_field, self.fields[target_faction][target_field].index(target_fighter), len(self.fields[target_faction][target_field])),
                                    'skill': i})
                return True
            