import pygame
import random

from unit import *
from block import *

class Defender(Unit):
    def __init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack):
        Unit.__init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack)

    def attack2(self): #augmentation constance de la defence prso
        self.defence = self.defence +2

    def attack3(self, target):
        target.health += 5