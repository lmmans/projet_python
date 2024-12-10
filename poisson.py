import pygame
import random

from unit import *
from block import *

class Poisson(Unit):
    def __init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack, additional_damage):
        Unit.__init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack, additional_damage)
        #self.bonus_applied = False  # Flag per bonus

        self.attack1_name = "Water Attack"
        self.attack2_name = "Trident attack"
        self.attack3_name = "Water Healing"
        self.attack4_name = " Tsunami Call"
        self.attack_methodes=["Attaque Normal", "Attack Proche"]

    def move(self, dx, dy,wall):
        """Déplace l'unité de dx, dy si possible."""
        if self.vitesse > 0 and self.team=="player":  # Vérifie si des déplacements sont possibles
            #if not self.eviter_mur():
                new_x = self.x + dx
                new_y = self.y + dy
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (new_x, new_y) not in WALL:
                # on controlle aussi si l'unitè se trouve sur les murs que on a construit
                    for mur in wall:
                        if (mur.x, mur.y) != (new_x, new_y):
                            self.x = new_x
                            self.y = new_y
                            self.vitesse -= 1
                    if not wall:
                        self.x = new_x
                        self.y = new_y
                        self.vitesse -= 1
        # je n'ai pas fait l'integration du mur pour les enemy
        if self.team=="enemy":
            new_x = self.x + dx
            new_y = self.y + dy
            if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (new_x, new_y) not in DONOTGO:
                self.x = new_x
                self.y = new_y


    def attack_ocean(self):
            degas = self.attack_power_base *4
            return degas
    
    def attack_normal(self):
         degas = self.attack_power_base
         return degas
    
    def attack1(self, target, wall, enemy_list):
        attack_minimum = 1
        if (self.x, self.y) not in RIVER:
            #attack_minimum = 1
            attack = self.attack_normal()
            degas = max(attack_minimum, attack - target.defence)
            target.health -= degas
        elif (self.x, self.y) in RIVER: #aumentation attack temporarire
            attack = self.attack_ocean()
            degas = max(attack_minimum, attack - target.defence)
            target.health -= degas
        if target.health <= 0:
            enemy_list.remove(target)

    #def attack2(self):
    #    pass

class Shark(Poisson):
    def __init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack, additional_damage):
        Poisson.__init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack, additional_damage)
        self.is_selected = False

        self.attack1_name = "Shark Attack"
        self.attack2_name = None
        self.attack3_name = None
        self.attack4_name = None