import pygame
import random

from unit import *
from block import *

class Defender(Unit):
    def __init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack, additional_damage):
        Unit.__init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack, additional_damage)

        self.attack1_name = "Guardian Attack"
        self.attack2_name = "Protector (Add defense)"
        self.attack3_name = "Curing Power"
        self.attack4_name = "Blue Fire (Add Power to Allies)"
        self.attack_methodes_enemies=["Attaque 1","Augmentation Defense","Curing Power","Augmentation Power"]

    def attack2(self): #augmentation constance de la defence prso
        self.defence = self.defence +3

    def attack3(self, player_list):
        for unit in player_list:
            if abs(self.x - unit.x) <= self.distance_attack and abs(self.y - unit.y) <= self.distance_attack:
                if unit != self:
                    unit.health += 5

    def power_allies(self, player_list):
        for unit in player_list:
            if abs(self.x - unit.x) <= self.distance_attack and abs(self.y - unit.y) <= self.distance_attack:
                if unit != self:
                    unit.attack_power_base += 2
    
        
