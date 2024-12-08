import pygame
import random

from unit import *
from block import *

class Defender(Unit):
    def __init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack, additional_damage):
        Unit.__init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack, additional_damage)

        self.attack1_name = "Protector"
        self.attack2_name = "Curing Power"
        self.attack3_name = "Blue Fire"
        self.attack4_name = " Eclipse" #Temp Name 

    def attack2(self): #augmentation constance de la defence prso
        self.defence = self.defence +2

    def attack3(self, target):
        target.health += 5

    ###temporaire
    def attack_normal(self):
        degas = self.attack_power_base
        return degas
    
    def attack_proche(self):
        degas = self.attack_power_base*7
        return degas

    """def attack4(self, target):
        attack_minimum = 1
        a = self.attack_normal()
        degas = max(attack_minimum, a - target.defence)
        target.additional_damage +=1
        #if abs(self.x - target.x) <= self.distance_attack and abs(self.y - target.y) <= self.distance_attack:
        target.health -= degas"""