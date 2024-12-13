import pygame
import random
from block import *

### Pour gener les mouvement ( par default personne peut aller dans les WALL et RIVER)
class Position:
    def __init__(self, x, y, vitesse):
        self.x = x
        self.y = y
        self.vitesse = vitesse

    def move(self, dx, dy, wall):
        """Déplace l'unité de dx, dy si possible."""
        if self.vitesse > 0:
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
        self.initial_speed= vitesse
    
    def attack_1(self):
        degas = self.attack_power_base 
        return degas        
   
    # Si attack < defence enemy au moins lui font 1 dega
    def attack1(self, wall, enemy_list):
        for enemy in enemy_list:
        # boucle pou attaquer tout les enemy
            if abs(self.x - enemy.x) <= self.distance_attack and abs(self.y - enemy.y) <= self.distance_attack:
                attack_minimum = 1
                a = self.attack_1()
                degas = max(attack_minimum, a - enemy.defence)
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
        
    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        if self.nom=="Athena":
            photo=pygame.image.load("ATHENA.jpeg")
            if self.is_selected:
                pygame.draw.rect(screen, RED, ((self.x - self.distance_attack) * CELL_SIZE,
                                (self.y - self.distance_attack)* CELL_SIZE, 
                                CELL_SIZE*(self.distance_attack*2 + 1), CELL_SIZE*(self.distance_attack*2 + 1)), 2)
        # creation carrè distance_attaque si unité selectioné
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
                
        elif self.nom=="Shark":
            photo=pygame.image.load("Shark.png")
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
              
    def attack_bombe(self, enemy_list, burnt_grass_list):
        for enemy in enemy_list:
            if abs(enemy.x - self.x) <= self.distance_attack and abs(enemy.y - self.y) <= self.distance_attack:         
                degas = 50 
                if enemy.x == self.x and enemy.y == self.y: # ememy sur la meme position
                    enemy.health -= degas
                else:      # enemy entre la distance d'action 
                    enemy.health -= (degas/2)
                if enemy.health <= 0:
                    enemy_list.remove(enemy)
        self.bombe_affected_zone(burnt_grass_list)

    def attack_trap(self, enemy_list, burnt_grass_list, bombe_list): 
        degas = 50
        for enemy in enemy_list:
            if enemy.x == self.x and enemy.y == self.y:         
                enemy.health -= degas
                self.bombe_affected_zone(burnt_grass_list)
                bombe_list.remove(self)  
                if enemy.health <= 0:
                    enemy_list.remove(enemy)
            else:
                pass
        return

    def bombe_affected_zone(self, burnt_grass_list):
        for dx in range(-1, 2):  
            for dy in range(-1, 2):  
                if (self.x+dx,self.y+dy)not in DONOTGO:
                    burnt_grass_list.append((self.x + dx, self.y + dy))

class Mur:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image=pygame.image.load("wall.png")
        self.is_selected = True

    def draw(self, screen): 
        if self.is_selected:
            scaled_image = pygame.transform.scale(self.image, (CELL_SIZE,CELL_SIZE))
            screen.blit(scaled_image, (self.x * CELL_SIZE, self.y * CELL_SIZE))

            
class Tresore():
    def __init__(self, x, y, nom):
        self.x = x
        self.y = y
        self.nom = nom
        self.is_selected = True
        self.treasure_yellow=pygame.image.load("Treasure.png")
        self.treasure_blue=pygame.image.load("TreasureBlue.png")
        self.treasure_blanc=pygame.image.load("TreasureBlanc.png")

    def draw(self, screen):  
        if self.nom == "Vitesse":
            if self.is_selected:
                scaled_image = pygame.transform.scale(self.treasure_yellow, (CELL_SIZE,CELL_SIZE))
                screen.blit(scaled_image, (self.x * CELL_SIZE, self.y * CELL_SIZE))
            
        if self.nom == "Strength":
            if self.is_selected:
                scaled_image = pygame.transform.scale(self.treasure_blue, (CELL_SIZE,CELL_SIZE))
                screen.blit(scaled_image, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        
        if self.nom == "Distance_attack":
            if self.is_selected:
                scaled_image = pygame.transform.scale(self.treasure_blanc, (CELL_SIZE,CELL_SIZE))
                screen.blit(scaled_image, (self.x * CELL_SIZE, self.y * CELL_SIZE))
    
    def bonus_vitesse(self, target):
        target.vitesse += 2
        return target.vitesse

    def bonus_attack(self, target):
        target.attack_power_base +=3

    def bonus_dist_attack(self, target):
        target.distance_attack += 1

    def spawn_tresore(self, tresore_on_map):
        if len(tresore_on_map) <= 6:
            casual_choise = random.randint(0, 15)
            position_x = random.randint(0, GRID_SIZE)
            position_y = random.randint(0, GRID_SIZE) 
            if casual_choise == 0:
                new_tresore = Tresore(position_x, position_y, "Vitesse")
                tresore_on_map.append(new_tresore)
            elif casual_choise == 1:
                new_tresore = Tresore(position_x, position_y,"Strength")
                tresore_on_map.append(new_tresore)
            elif casual_choise == 2:
                new_tresore = Tresore(position_x, position_y, "Distance_attack")
                tresore_on_map.append(new_tresore)

    def compare_position_tresore(self, tresore_on_map, selected_unit, initial_speed, index):
        if len(tresore_on_map) >= 1:
            for tresore in tresore_on_map:
                if tresore.x == selected_unit.x and tresore.y == selected_unit.y:
                    if tresore.nom == "Vitesse":
                        Tresore.bonus_vitesse(self,selected_unit)
                        initial_speed[index] = selected_unit.vitesse

                    elif tresore.nom == "Strength":
                            Tresore.bonus_attack(self, selected_unit)
                          
                    elif tresore.nom == "Distance_attack":
                            Tresore.bonus_dist_attack(self, selected_unit)

                    tresore_on_map.remove(tresore)
                    return True  # indique si le bonus a été appliqué
        return False  # Pas des bonus appliqué
