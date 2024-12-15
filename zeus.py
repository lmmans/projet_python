import pygame
import random

from unit import *
from block import *

class Assasin(Unit):
    def __init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack, additional_damage):
        Unit.__init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack, additional_damage)

        self.attack1_name = "Earthquake"
        self.attack2_name = "Thunderbolt Sword"
        self.attack3_name = "Storm Teleporation"
        self.attack4_name = " Lightning Attack"
        self.attack_methodes_enemies=["Attack 1","Attaque Foudre","Attaque Proche","Attack Teleportation"]
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
                enemy.additional_damage +=5
                enemy.health -= degas 
                if enemy.health <= 0:
                    enemy_list.remove(enemy)

    def teleportation(self,direction=''):
            vitesse=5
            dx, dy = 0, 0  
            horizontal = False 
            not_acted=True
            if self.team=="player":
                while not_acted:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_LEFT:
                                dx = -vitesse
                                horizontal = True
                                not_acted=False

                            elif event.key == pygame.K_RIGHT:
                                dx = vitesse
                                horizontal = True
                                not_acted=False

                            elif event.key == pygame.K_UP:
                                dy = -vitesse
                                not_acted=False

                            elif event.key == pygame.K_DOWN:
                                dy = vitesse
                                not_acted=False   

            else:
                if direction=="Up":
                    dy=-vitesse
                    horizontal=False
                elif direction =="Down":
                    dy=+vitesse
                    horizontal=False
                elif direction=="Right":
                    dx=vitesse
                    horizontal=True
                elif direction=="Left":
                    dx=-vitesse
                    horizontal=True
                
                
            if horizontal:
                new_x = self.x + dx
                while (new_x, self.y) in DONOTGO:
                    new_x-=1
                if 0 <= new_x < GRID_SIZE and 0 <= self.y < GRID_SIZE and (new_x, self.y) not in DONOTGO:
                    self.x=new_x
                    
            else:
                new_y = self.y + dy
                print(new_y)
                while (self.x, new_y) in DONOTGO:
                    new_y-=1
                if 0 <= self.x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (self.x, new_y) not in DONOTGO:
                    self.y=new_y
    