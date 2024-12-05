import pygame
import random

from Unit import *
from block import *

class Oiseau(Unit):
    def __init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack, degas):
        Unit.__init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack, degas)
        self.bonus_attack = 3
        self.bonus_applied = False  # Flag per bonus
        self.photo=pygame.image.load("ATHENA.jpeg")

    ##def reset_bonus(self):
        ##self.attack_power = self.attack_power_base
        ##return self.attack_power 
    ##def attack_1(self):
        ##self.degas = self.attack_power_base 
        ##return self.degas     

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
### j'amerai bien lui donner un bonus attack quand elle els sur le mur (sinon est inutil monter sur les murs)
### je n'y arrive pas a enlever le bonus quand elle decende 
### Problem, le bonus s'ajout chaque fois que alle marche sur le mur
                    #if (new_x, new_y) in WALL:
                    #   self.attack_power_base +=3
### Code proposè par chat gpt mais je n'arrive pas a le fair marcher
               # Applica il bonus se si trova su un muro

                    ##if (self.x, self.y) in WALL and not self.bonus_applied:
                        ##self.attack_power = self.attack_power_base + self.bonus_attack  # Aggiunge il bonus
                        ##self.bonus_applied = True  # Segna che il bonus è stato applicato
                    ##elif (self.x, self.y) not in WALL:
                        ##self.reset_bonus()  # Resetta il bonus se non è su un muro"""
