
class auto:
    def __init__(self, controller):
        self.controller = controller

    def next(self):
        fighter = self.controller.prepared_fighter[0]
        while fighter.ap >= 2:
            for i in self.controller.all_fighters:
                if i.faction != fighter.faction:
                    enemy = i
                    break
            self.controller.cast(fighter.c['skills'][0]['name'], enemy.faction, enemy.field, enemy)
        self.controller.skip()
        