import pygame
import random

from unit import *
from block import *

class Oiseau(Unit):
    def __init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack):
        Unit.__init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack)
        self.bonus_attack = 3
        self.bonus_applied = False  # Flag per bonus
        self.photo=pygame.image.load("ATHENA.jpeg")    

### Donne la possibilitè de passer sur les WALL
    def move(self, dx, dy):
        """Déplace l'unité de dx, dy si possible."""
        if self.vitesse > 0:  # Vérifie si des déplacements sont possibles
            #if not self.eviter_mur():
                new_x = self.x + dx
                new_y = self.y + dy
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (new_x, new_y) not in RIVER:
                    self.x = new_x
                    self.y = new_y
                    self.vitesse -= 1  # Réduit la vitesse après chaque mouvement

    def attack_volant(self):
         degas = self.attack_power_base *4
         return degas
    
    def attack_normal(self):
         degas = self.attack_power_base
         return degas
    
    def attack1(self, target):
        attack_minimum = 1
        if (self.x, self.y) not in WALL:
            #attack_minimum = 1
            attack = self.attack_normal()
            degas = max(attack_minimum, attack - target.defence)
            target.health -= degas
        elif (self.x, self.y) in WALL: #aumentation attack temporarire
            attack = self.attack_volant()
            degas = max(attack_minimum, attack - target.defence)
            target.health -= degas

    def attack2(self):
        pass
              
