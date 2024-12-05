import pygame
import random
from block import *

### Pour gener les mouvement ( par default personne peut aller dans les WALL et RIVER)
class Position:
    def __init__(self, x, y, vitesse):
        self.x = x
        self.y = y
        self.vitesse = vitesse

    def move(self, dx, dy):
        """Déplace l'unité de dx, dy si possible."""
        #self.vitesse = self.vitesse
        if self.vitesse > 0:  # Vérifie si des déplacements sont possibles
            new_x = self.x + dx
            new_y = self.y + dy
            if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (new_x, new_y) not in DONOTGO:
                self.x = new_x
                self.y = new_y
                self.vitesse -= 1  # Réduit la vitesse après chaque mouvement

class Unit(Position):
    def __init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack, degas):
        Position.__init__(self, x, y, vitesse)
        self.nom = nom
        self.health = health
        self.attack_power_base = attack_power_base
        self.defence = defence
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False
        self.distance_attack = distance_attack
        self.degas = degas
    
    
    def attack_1(self):
        self.degas = self.attack_power_base 
        return self.degas        
   
### Si attack < defence enemy au moins lui font 1 dega
    def attack1(self, target):
        attack_minimum = 1
        a = self.attack_1()
        degas = max(attack_minimum, a - target.defence)
        #if abs(self.x - target.x) <= self.distance_attack and abs(self.y - target.y) <= self.distance_attack:
        target.health -= degas
        

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        color = BLUE if self.team == 'player' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
                           2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

### Class pour chaque personnage



### class defender et assassin cree mais je n'ai pas encor fait les attack
class Defender(Unit):
    def __init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack, degas):
        Unit.__init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack, degas)

class Assasin(Unit):
    def __init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack, degas):
        Unit.__init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack, degas)
