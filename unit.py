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
        #temp = self.vitesse
        #print(temp)
        if self.vitesse > 0:
            new_x = self.x + dx
            new_y = self.y + dy
            if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (new_x, new_y) not in DONOTGO:
                self.x = new_x
                self.y = new_y
                self.vitesse -= 1        


class Unit(Position):
    def __init__(self, x, y, vitesse, nom, health, attack_power_base, defence, team, distance_attack, additional_damage):
        Position.__init__(self, x, y, vitesse)
        self.nom = nom
        self.health = health
        self.attack_power_base = attack_power_base
        self.defence = defence
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False
        self.distance_attack = distance_attack
        self.additional_damage = additional_damage
    
    
    def attack_1(self):
        degas = self.attack_power_base 
        return degas        
   
    # Si attack < defence enemy au moins lui font 1 dega
    def attack1(self, target):
        attack_minimum = 1
        a = self.attack_1()
        degas = max(attack_minimum, a - target.defence)
        target.health -= degas
        

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        if self.nom=="Athena":
            photo=pygame.image.load("ATHENA.jpeg")
        # creation carrè distance_attaque si unité selectioné
            if self.is_selected:
                pygame.draw.rect(screen, RED, ((self.x - self.distance_attack) * CELL_SIZE,
                                (self.y - self.distance_attack)* CELL_SIZE, 
                                CELL_SIZE*(self.distance_attack*2 + 1), CELL_SIZE*(self.distance_attack*2 + 1)), 2)
        elif self.nom=="Poseidon":
            photo=photo=pygame.image.load("poseidon.jpeg")
            if self.is_selected:
                pygame.draw.rect(screen, RED, ((self.x - self.distance_attack) * CELL_SIZE,
                                (self.y - self.distance_attack)* CELL_SIZE, 
                                CELL_SIZE*(self.distance_attack*2 + 1), CELL_SIZE*(self.distance_attack*2 + 1)), 2)
        elif self.nom=="Zeus":
            photo=pygame.image.load("zeus.jpeg")
            if self.is_selected:
                pygame.draw.rect(screen, RED, ((self.x - self.distance_attack) * CELL_SIZE,
                                (self.y - self.distance_attack)* CELL_SIZE, 
                                CELL_SIZE*(self.distance_attack*2 + 1), CELL_SIZE*(self.distance_attack*2 + 1)), 2)
        elif self.nom=="Hecate":
            photo=pygame.image.load("hecate.png")
            if self.is_selected:
                pygame.draw.rect(screen, RED, ((self.x - self.distance_attack) * CELL_SIZE,
                                (self.y - self.distance_attack)* CELL_SIZE, 
                                CELL_SIZE*(self.distance_attack*2 + 1), CELL_SIZE*(self.distance_attack*2 + 1)), 2)

        scaled_image = pygame.transform.scale(photo, (CELL_SIZE,CELL_SIZE))
        screen.blit(scaled_image, (self.x * CELL_SIZE, self.y * CELL_SIZE))

class Bombe:
    def __init__(self, x, y, distance_attack,team):
        self.x = x
        self.y = y
        self.depart_x = x
        self.depart_y = y
        self.distance_attack = distance_attack
        self.team=team
        
        self.is_selected = True


    def draw(self, screen):   
        if self.is_selected:
            if self.team=="player":
                bomb_color=GREEN
            else:
                bomb_color= YELLOW

            pygame.draw.rect(screen, bomb_color, ((self.x - 0.25) * CELL_SIZE,
                (self.y - 0.25) * CELL_SIZE, CELL_SIZE*1.5, CELL_SIZE*1.5), 4)
    
           
    def move(self, dx, dy):
        "Déplace l'unité de dx, dy, restreint à une zone 3x3."
        new_x = self.x + dx
        new_y = self.y + dy
        # Pour controler que le mouvement soit en un carrè 3*3
        if (self.depart_x - 3 <= new_x <= self.depart_x + 3 and
            self.depart_y - 3 <= new_y <= self.depart_y + 3) and self.team=="player":
            if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                self.x = new_x
                self.y = new_y
            
    
    def attack_bombe(self, enemy,enemy_list):
        degas = 50 
        if enemy.x == self.x and enemy.y == self.y: # ememy sur la meme position
            enemy.health -= degas
        else:      # enemy entre la distance d'action 
            enemy.health -= (degas/2)
        if enemy.health <= 0:
            enemy_list.remove(enemy)

    def bombe_affected_zone(self, burnt_grass_list):
        for dx in range(-1, 2):  
            for dy in range(-1, 2):  
                if (self.x+dx,self.y+dy)not in DONOTGO:
                    burnt_grass_list.append((self.x + dx, self.y + dy))

        

