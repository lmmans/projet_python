import pygame
import random

from unit import *
from block import *

class Assasin(Unit):
    def __init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack, additional_damage):
        Unit.__init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack, additional_damage)

        self.attack1_name = "Earthquake"
        self.attack2_name = "Thunderbolt Sword"
        self.attack3_name = "Lighting Attack"
        self.attack4_name = " Storm Attack"
        self.attack_methodes=["Attaque Normal", "Attack Proche","Attack BOMB"]
        self.throw_bomb=True

    def attack_normal(self):
        degas = self.attack_power_base
        return degas
    
    def attack_proche(self):
        degas = self.attack_power_base*7
        return degas
    
    def attack2(self, enemy_list):
        for enemy in self.enemy_units:
            if abs(self.x - enemy.x) <= 1 and abs(self.y - enemy.y) <= 1:
                attack_minimum = 1
                a = self.attack_proche()
                degas = max(attack_minimum, a - enemy.defence)
                #if abs(self.x - target.x) <= self.distance_attack and abs(self.y - target.y) <= self.distance_attack:
                enemy.health -= degas
                if enemy.health <= 0:
                    enemy_list.remove(enemy)

    def attack_foudre(self, enemy_list):
        for enemy in enemy_list:
            if abs(self.x - enemy.x) <= self.distance_attack and abs(self.y - enemy.y) <= self.distance_attack:
                attack_minimum = 1
                a = self.attack_normal()
                degas = max(attack_minimum, a - enemy.defence)
                enemy.additional_damage +=20
                enemy.health -= degas 
                if enemy.health <= 0:
                    enemy_list.remove(enemy)

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