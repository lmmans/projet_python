import pygame
import random

from unit import *
from block import *

class Poisson(Unit):
    def __init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack, degas):
        Unit.__init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack, degas)
        self.bonus_attack = 3
        self.bonus_applied = False  # Flag per bonus

    def move(self, dx, dy):
        """Déplace l'unité de dx, dy si possible."""
        if self.vitesse > 0:  # Vérifie si des déplacements sont possibles
            #if not self.eviter_mur():
                new_x = self.x + dx
                new_y = self.y + dy
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (new_x, new_y) not in WALL:
                    self.x = new_x
                    self.y = new_y
                    self.vitesse -= 1  # Réduit la vitesse après chaque mouvement
### meme chose avec lui dans RIVER
                    if (new_x, new_y) in RIVER:
                       self.attack_power_base +=3
