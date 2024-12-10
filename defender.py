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
        self.attack_methodes=["Attaque 1", "Attack 2","Attack 3","Attack 4"]

    def attack2(self): #augmentation constance de la defence prso
        self.defence = self.defence +2

    def attack3(self, target):
        target.health += 5

    def attack4(self, target):
        target.attack_power_base += 4

    def move(self, dx, dy,wall):
        """Déplace l'unité de dx, dy si possible."""
        if self.vitesse > 0 and self.team=="player":  # Vérifie si des déplacements sont possibles
                new_x = self.x + dx
                new_y = self.y + dy
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (new_x, new_y) not in DONOTGO:
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
    
    def teleportation(self):
        self.vitesse=5
        dx, dy = 0, 0  
        horizontal = False 
        not_acted=True
        while not_acted:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        dx = -5
                        horizontal = True
                        not_acted=False

                    elif event.key == pygame.K_RIGHT:
                        dx = 5
                        horizontal = True
                        not_acted=False

                    elif event.key == pygame.K_UP:
                        dy = -5
                        not_acted=False

                    elif event.key == pygame.K_DOWN:
                        dy = 5
                        not_acted=False

            
        if horizontal:
            new_x = self.x + dx
            while (new_x, self.y) in DONOTGO:
                new_x-=1
            if 0 <= new_x < GRID_SIZE and 0 <= self.y < GRID_SIZE and (new_x, self.y) not in DONOTGO:
                self.x=new_x
        else:
            new_y = self.y + dy
            if 0 <= self.x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (self.x, new_y) not in DONOTGO:
                self.y=new_y

        

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