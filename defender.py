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
        self.attack_methodes=["Attaque Normal", "Attack Proche","Attack BOMB"]

    def attack2(self): #augmentation constance de la defence prso
        self.defence = self.defence +2

    def attack3(self, target):
        target.health += 5

    def attack4(self, target):
        target.attack_power_base += 4

    def move(self, dx, dy, wall):
        """Déplace l'unité de dx, dy si possible."""
        if self.vitesse > 0 and self.team=="player":  # Vérifie si des déplacements sont possibles
            #if not self.eviter_mur():
            new_x = self.x + dx
            new_y = self.y + dy
            if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (new_x, new_y) not in DONOTGO:
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
        if self.team=="enemy":
            new_x = self.x + dx
            new_y = self.y + dy
            if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (new_x, new_y) not in DONOTGO:
                self.x = new_x
                self.y = new_y

    ###temporaire
"""    def attack_normal(self):
        degas = self.attack_power_base
        return degas
    
    def attack_proche(self):
        degas = self.attack_power_base*7
        return degas

    def attack4(self, target):
        attack_minimum = 1
        a = self.attack_normal()
        degas = max(attack_minimum, a - target.defence)
        target.additional_damage +=1
        #if abs(self.x - target.x) <= self.distance_attack and abs(self.y - target.y) <= self.distance_attack:
        target.health -= degas"""