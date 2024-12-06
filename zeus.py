import pygame
import random

from unit import *
from block import *

class Assasin(Unit):
    def __init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack):
        Unit.__init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack)

    def attack_normal(self):
        degas = self.attack_power_base
        return degas
    
    def attack_proche(self):
        degas = self.attack_power_base*7
        return degas
    
    def attack2(self, target):
        attack_minimum = 1
        a = self.attack_proche()
        degas = max(attack_minimum, a - target.defence)
        #if abs(self.x - target.x) <= self.distance_attack and abs(self.y - target.y) <= self.distance_attack:
        target.health -= degas