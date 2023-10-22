import pygame as pg

class fighter:
    def __init__(self, properties):
        self.initial = properties
        self.current = self.initial.copy()
        self.hp = self.current['maxhp']
        self.mp = self.current['maxmp']
        self.ap = self.current['maxap']
        self.effects = []

    @property
    def i(self):
        return self.initial
    
    @property
    def c(self):
        return self.current