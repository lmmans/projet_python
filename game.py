import pygame
import random

from unit import *
from block import *
from oiseau import *
from poisson import *
from defender import * 
from zeus import *


class Game:

    def __init__(self, screen):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        self.screen = screen
        self.player_units = [Oiseau(3, 0, 4,"Athena", 80, 2, 5, 'player', 3, 0),
                             Poisson(1, 0, 4,"Poseidon", 80, 8, 5, 'player', 3, 0),
                             Defender(2, 0, 4,"Hecate", 80, 20, 5, 'player', 2, 0),
                             Assasin(4, 0, 6, "Zeus", 80, 10, 5, 'player', 1, 0)
                             ]

        self.enemy_units = [Defender(3, 11, 4,"Hecate", 100, 50, 5, 'enemy', 1, 0),
                            Assasin(13, 14, 4,"Zeus", 100, 8, 5, 'enemy', 2, 0)]
        
        self.initial_speed = [player.vitesse for player in self.player_units]

        #Génération de la riviere
        self.generateriver=GenerateBlocks(ROWS,COLUMNS,'river')
        self.river_blocks = self.generateriver.create_river()

        #Génération des murs
        self.generatewalls=GenerateBlocks(ROWS,COLUMNS,'wall')
        self.wall_blocks=self.generatewalls.create_wall()

        #Génération de la pelouse
        self.generategrass=GenerateBlocks(ROWS,COLUMNS,'grass')
        self.grass_blocks=self.generategrass.create_grass()
        
        self.font = pygame.font.SysFont('Arial', 16)

        self.bombe_unit = []
        self.bombe_enemy= []
        self.burnt_grass= []
        self.traps_placed=[]
        self.wall = []
        self.tresore_on_map = []

    def show_attack_options(self, selected_unit, x, y):
        # List of potential attacks
        attacks = [
            ("A", selected_unit.attack1_name),
            ("S", getattr(selected_unit, "attack2_name", None)),
            ("D", getattr(selected_unit, "attack3_name", None)),
            ("F", getattr(selected_unit, "attack4_name", None)),
        ]

        # Prepare the text to render, filtering out None or missing attacks
        attack_text = [f"Player: {selected_unit.nom}"]
        attack_text += [f"{key}: {name}" for key, name in attacks if name is not None]

        # Render the text
        for i, line in enumerate(attack_text):
            text_surface = self.font.render(line, True, WHITE)
            self.screen.blit(text_surface, (x, y + i * 20))


    def handle_player_turn(self):
        """Tour du joueur"""
        #print(self.initial_speed)
        #print("coucou")
        i = 0
        for index, selected_unit in enumerate(self.player_units):
            
            selected_unit.vitesse = self.initial_speed[i]
            #print(self.initial_speed[i])
            i += 1
            #print(selected_unit.vitesse)
                ###essaier de le faire bouger 2 pas a la fois
               # selected_unit.vitesse = 4
            #if selected_unit.nom == "Poseidon":
            #    selected_unit.vitesse = 3
            #if selected_unit.nom=="Hecate":
            #    selected_unit.vitesse=5

            # Tant que l'unité n'a pas terminé son tour
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()
            while not has_acted:
                # Important: cette boucle permet de gérer les événements Pygame
                for event in pygame.event.get():

                    # Gestion de la fermeture de la fenêtre
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    # Gestion des touches du clavier
                    if event.type == pygame.KEYDOWN:
                        """ 
                        if selected_unit.nom=="Athena":
                            steps=5
                        elif selected_unit.nom=="Poseidon":
                            steps=5
                        else:
                            steps=1
                        """

                        # Déplacement (touches fléchées)
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1

                        if selected_unit.vitesse > 0:
                            selected_unit.move(dx, dy,self.wall)
                            self.flip_display()

                    # avant de commencer les attaques on regard si l'unitè est sur un tresor
                        if len(self.tresore_on_map) >= 1:
                            for tresore in self.tresore_on_map:
                                if tresore.x == selected_unit.x and tresore.y == selected_unit.y:
                                    if tresore.nom == "Vitesse":
                                        tresore.bonus_vitesse(selected_unit)
                                        self.initial_speed[index] = selected_unit.vitesse
                                        self.tresore_on_map.remove(tresore)
                                        has_acted = True
                                        #self.initial_speed.append(new_shark.vitesse)
                                        #self.initial_speed[i]
                                    elif tresore.nom == "Strength":
                                        tresore.bonus_attack(selected_unit)
                                        self.tresore_on_map.remove(tresore)
                                        has_acted = True
                                    elif tresore.nom == "Distance_attack":
                                        tresore.bonus_dist_attack(selected_unit)
                                        self.tresore_on_map.remove(tresore)
                                        has_acted = True
                                    selected_unit.is_selected = False
                                    self.flip_display()
                                else:
                                    has_acted = False

                    #ATTAQUES
                        #attaque "a" (attque multiple base pour tous)
                        if event.key == pygame.K_a:
                            for enemy in self.enemy_units:
                                # boucle pou attaquer tout les enemy
                                if abs(selected_unit.x - enemy.x) <= selected_unit.distance_attack and abs(selected_unit.y - enemy.y) <= selected_unit.distance_attack:
                                    selected_unit.attack1(enemy, self.wall, self.enemy_units)
                                    #if enemy.health <= 0:
                                        #self.enemy_units.remove(enemy)
                            #changer l'unité apre l'attaque
                            has_acted = True
                            selected_unit.is_selected = False

                        # attaque "s" (Hecate -> defene +2)                                         
                        elif event.key == pygame.K_s:
                            if selected_unit.nom == "Hecate":
                                selected_unit.attack2()
                                has_acted = True
                                selected_unit.is_selected = False
                            elif selected_unit. nom == "Zeus":
                                for enemy in self.enemy_units:
                                    if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                        selected_unit.attack2(enemy, self.enemy_units)
                                        has_acted = True
                                        selected_unit.is_selected = False
                            else:
                                has_acted = False

                        # attaque "d" (Hecate -> health +5 allies)
                        elif event.key == pygame.K_d:
                            if selected_unit.nom == "Athena":
                                # lititation a 4 fois
                                if len (self.wall) <= 3:
                                    new_wall = Mur(selected_unit.x, selected_unit.y)
                                    self.wall.append(new_wall)
                                    has_acted = True
                                    selected_unit.is_selected = False 
                                else:
                                    has_acted = False 
                            if selected_unit.nom == "Poseidon":
                                if len (self.player_units) <= 6:
                                    new_shark = Shark(selected_unit.x +1, selected_unit.y + 1, 6, "Shark", 10, 15, 5, 'player', 1, 0)
                                    self.player_units.append(new_shark)
                                    self.initial_speed.append(new_shark.vitesse)
                                    #selected_unit.vitesse = self.initial_speed[i]
                                    has_acted = True
                                    selected_unit.is_selected = False
                                else:
                                    has_acted = False
                            # boucle pour tous les allies... 
                            if selected_unit.nom == "Hecate":
                                for unit in (self.player_units):
                                    # ...sauf lui
                                    if unit != selected_unit:
                                        if abs(selected_unit.x - unit.x) <= selected_unit.distance_attack and abs(selected_unit.y - unit.y) <= selected_unit.distance_attack:
                                            selected_unit.attack3(unit)  
                                    has_acted = True
                                    selected_unit.is_selected = False

                        # attque "f" (Athena, Zeus -> attaque siblé)
                        elif event.key == pygame.K_f:
                            if selected_unit.nom == "Athena" or selected_unit.nom == "Poseidon":
                                # creation unité dans la liste ""self.bombe_unit"
                                new_bombe = Bombe(selected_unit.x, selected_unit.y, 2,"player")
                                self.bombe_unit.append(new_bombe)
                                #self.bombe_unit.draw(self.screen)
                                self.flip_display()
                                self.handle_bombe_turn(new_bombe,selected_unit)
                                        
                            elif selected_unit.nom == "Hecate":
                                for unit in (self.player_units):
                                    if unit != selected_unit:
                                        if abs(selected_unit.x - unit.x) <= selected_unit.distance_attack and abs(selected_unit.y - unit.y) <= selected_unit.distance_attack:
                                            selected_unit.attack4(unit)

                            elif selected_unit.nom == "Zeus":
                                for enemy in (self.enemy_units):
                                        if abs(selected_unit.x - enemy.x) <= selected_unit.distance_attack and abs(selected_unit.y - enemy.y) <= selected_unit.distance_attack:
                                            selected_unit.attack4(enemy, self.enemy_units) 
                                        #if enemy.health == 0:
                                            #self.enemy_units.remove(enemy)  
                            has_acted = True
                            selected_unit.is_selected = False

                        elif event.key == pygame.K_t:
                            if selected_unit.nom=="Hecate":
                                selected_unit.teleportation()

                                has_acted=True
                                selected_unit.is_selected= False

                        elif event.key == pygame.K_SPACE:
                            has_acted = True
                            selected_unit.is_selected = False

    # le turn de la Bombe est actioné seulement si on utilise la touche "f"
    def handle_bombe_turn(self, bombe_unit, selected_unit):
            """Tour de la bombe"""
            has_acted = False # boucle le cicle entier      
            while not has_acted:   
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                                dy = 1

                    #appelle a la def move de la bombe
                        if not has_acted:  # Permette di muovere solo finché non è stata fatta un'azione
                            bombe_unit.move(dx, dy)
                            self.flip_display()

                # touche SPACE pour attaquer ou installer la bombe
                        if event.key == pygame.K_SPACE:

                # Zeus -> lance la bombe, la bombe est detruit apres l'attaque
                # aussi si la cible n'est pas touchè
                                if selected_unit.nom == "Poseidon":
                                    for enemy in self.enemy_units:
                                        if abs(enemy.x - bombe_unit.x) <= bombe_unit.distance_attack and abs(enemy.y - bombe_unit.y) <= bombe_unit.distance_attack: 
                                            bombe_unit.attack_bombe(enemy,self.enemy_units)
                                            bombe_unit.bombe_affected_zone(self.burnt_grass)
                                        else:
                                            bombe_unit.bombe_affected_zone(self.burnt_grass)
                                        self.bombe_unit.remove(bombe_unit)  
                                        self.flip_display()
                                        return 
                                    

                                    if not enemy:
                                            bombe_unit.bombe_affected_zone(self.burnt_grass)
                                            self.bombe_unit.remove(bombe_unit) 
                                            self.flip_display()
                                            return
                                    
                # Athena -> installe la bombe (trap) au sol
                # trap detrite seulement si l'enemy la touche                    
                                elif selected_unit.nom == "Athena":
                                    for enemy in self.enemy_units:
                                        if enemy.x == bombe_unit.x and enemy.y == bombe_unit.y:
                                            bombe_unit.attack_bombe(enemy,self.enemy_units)
                                            bombe_unit.bombe_affected_zone(self.burnt_grass)
                                            self.bombe_unit.remove(bombe_unit) #remouve la bombe apres l'attaque
                                            self.flip_display()
                                        else:
                                            self.flip_display()
                                    return
                                


    def move_towards_target(self,enemy, target, NOMove):
        
        possible_moves = []

        
        if (enemy.x + 1, enemy.y) not in NOMove:
            possible_moves.append((1, 0))  # Move right

        
        if (enemy.x - 1, enemy.y) not in NOMove:
            possible_moves.append((-1, 0))  # Move left

        
        if (enemy.x, enemy.y + 1) not in NOMove:
            possible_moves.append((0, 1))  # Move down

        
        if (enemy.x, enemy.y - 1) not in NOMove:
            possible_moves.append((0, -1))  # Move up

        
        if (enemy.x + 1, enemy.y - 1) not in NOMove:
            possible_moves.append((1, -1))  # Move right and up

        
        if (enemy.x + 1, enemy.y + 1) not in NOMove:
            possible_moves.append((1, 1))  # Move right and down

        
        if (enemy.x - 1, enemy.y - 1) not in NOMove:
            possible_moves.append((-1, -1))  # Move left and up

        
        if (enemy.x - 1, enemy.y + 1) not in NOMove:
            possible_moves.append((-1, 1))  # Move left and down

        
        if possible_moves:
            
            best_moves = []
            min_distance = float('inf')

            for dx, dy in possible_moves:
                new_x = enemy.x + dx
                new_y = enemy.y + dy
                distance_to_target = abs(new_x - target.x) + abs(new_y - target.y)

                
                if distance_to_target < min_distance:
                    best_moves = [(dx, dy)]
                    min_distance = distance_to_target
                elif distance_to_target == min_distance:
                    best_moves.append((dx, dy))

            dx, dy = random.choice(best_moves)
            return dx,dy
        else:
            dx,dy=0
            return dx,dy
        
    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""
        for enemy in self.enemy_units:
            ## j'ai essaie de remetre ici l'attaque de Zeus me ne marche pas
            enemy.health -= enemy.additional_damage
            if enemy.health <= 0:
                self.enemy_units.remove(enemy) 
 
            self.flip_display()
            # Déplacement aléatoire
            target = random.choice(self.player_units)
            if target.nom=="Athena":
                move_not_possible=RIVER
            elif target.nom=="Poseidon":
                move_not_possible=WALL
            else: 
                move_not_possible=DONOTGO
            
            
            dx,dy=self.move_towards_target(enemy,target,move_not_possible)
            enemy.move(dx,dy, self.wall)
            print(f"{enemy.nom}:{dx,dy}")
                 
            #pendant le tour de l'enemy on controlle si il est sur la trap ou no
            if self.bombe_unit:
            # [:] -> scansion de tous les trap et verification coordonnè avant de la detruire
                for bombe in self.bombe_unit[:]:
                    if enemy.x == bombe.x and enemy.y == bombe.y:
                        bombe.attack_bombe(enemy,self.enemy_units)
                        bombe.bombe_affected_zone(self.burnt_grass)
                        self.bombe_unit.remove(bombe)
                        self.flip_display()
                    else:
                        self.flip_display()

            attack_methods =enemy.attack_methodes
            chosen_attack = random.choice(attack_methods)
            
            """ 
            #DEBUG

            print(target.nom,chosen_attack)
            print(f"La longeur de la liste est :{len(self.player_units)}")
            if len(self.player_units)==5:
                print("dans la boucle")
                if enemy.nom== "Zeus":
                    target=self.player_units[4]
                    chosen_attack="Attack Proche"
                    print(target)
            """
            

            if abs(enemy.x - target.x) <= enemy.distance_attack and abs(enemy.y - target.y) <= enemy.distance_attack:
                if chosen_attack == "Attack BOMB":
                    if hasattr(enemy, "throw_bomb") and enemy.throw_bomb:
                            # Decide target location for the bomb (Avoid Having 100% Precision each time)
                        bomb_target_x = random.choice([target.x + 1, target.x - 1, target.x])
                        bomb_target_y = random.choice([target.y + 1, target.y - 1, target.y])
                            # Place a bomb at the target location
                        new_bomb = Bombe(bomb_target_x, bomb_target_y,enemy.distance_attack,enemy.team)
                        new_bomb.move(bomb_target_x, bomb_target_y)
                        new_bomb.attack_bombe(target,self.player_units)
                        new_bomb.bombe_affected_zone(self.burnt_grass)
                        self.bombe_enemy.append(new_bomb)
                        self.flip_display()
                        if self.bombe_enemy:
                            self.bombe_enemy.remove(self.bombe_enemy[-1])
                        continue  # Enemy turn ends after throwing a bomb
                else:
                    if chosen_attack=="Attack Proche":
                        if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                                    
                            degas=enemy.attack_normal()
                            target.health-=degas
                    if chosen_attack=="Attack Loin":
                        if abs(enemy.x - target.x) <= enemy.distance_attack and abs(enemy.y - target.y) <= enemy.distance_attack:
                            enemy.attack1(target, WALL, self.player_units)
                            if target.health <= 0:
                                self.player_units.remove(target)
                    if chosen_attack=="Attack Volant":
                        pass
    
    def handle_tresore_turn(self):
        if len(self.tresore_on_map) <= 6:
            casual_choise = random.randint(0, 3)
            position_x = random.randint(0, GRID_SIZE)
            position_y = random.randint(0, GRID_SIZE) 
            print(casual_choise)
            if casual_choise == 0:
                new_tresore = Tresore(position_x, position_y, "Vitesse")
                self.tresore_on_map.append(new_tresore)
                self.flip_display()
            elif casual_choise == 1:
                new_tresore = Tresore(position_x, position_y,"Strength")
                self.tresore_on_map.append(new_tresore)
                self.flip_display()
            elif casual_choise == 2:
                new_tresore = Tresore(position_x, position_y, "Distance_attack")
                self.tresore_on_map.append(new_tresore)
                self.flip_display()


    def draw_health_as_hearts(self, unit, x_offset, y_offset,team):
        max_health = 100  
        heart_size = 20  
        num_hearts = 10  

        filled_hearts = (unit.health / max_health) * num_hearts
        full_hearts = int(filled_hearts)  
        half_heart = filled_hearts - full_hearts >= 0.5
    
        if team=="enemy":
            heart_color=GREEN
        elif team =="player":
            heart_color=RED
        
        for i in range(full_hearts):
            heart_rect = pygame.Rect(x_offset + i * (heart_size + 5), y_offset, heart_size, heart_size)
            pygame.draw.rect(self.screen, heart_color, heart_rect)  

        if half_heart:
            half_heart_rect = pygame.Rect(x_offset + full_hearts * (heart_size + 5), y_offset, heart_size // 2, heart_size)
            pygame.draw.rect(self.screen, heart_color, half_heart_rect)  # Draw the left half
            empty_heart_rect = pygame.Rect(
                x_offset + full_hearts * (heart_size + 5) + heart_size // 2, 
                y_offset, 
                heart_size // 2, 
                heart_size
            )
            pygame.draw.rect(self.screen, (100, 100, 100), empty_heart_rect)  # Draw the right half as empty

        for i in range(full_hearts + (1 if half_heart else 0), num_hearts):
            heart_rect = pygame.Rect(x_offset + i * (heart_size + 5), y_offset, heart_size, heart_size)
            pygame.draw.rect(self.screen, (100, 100, 100), heart_rect) 

    def is_enemy_visible(self):
        visible = []

        for player in self.player_units:
            if 0 <= player.x <= 2 and 0 <= player.y <= 1:
                zones = 1
                square_ranges = [(0, 5, 0, 6)]

            elif 0 <= player.x <= 2 and 2 <= player.y <= 5:
                zones = 2
                square_ranges = [(0, 5, 0, 6), (0, 14, 2, 5)]

            elif 3 <= player.x <= 4 and 2 <= player.y <= 5:
                zones = 3
                square_ranges = [(0, 5, 0, 6), (0, 14, 2, 5), (3, 5, 0, 14)]

            elif 3 <= player.x <= 4 and 0 <= player.y <= 1:
                zones = 2
                square_ranges = [(0, 5, 0, 6), (3, 5, 0, 14)]

            elif 6 <= player.x <= 10 and 0 <= player.y <= 1:
                zones = 1
                square_ranges = [(5, 14, 0, 9)]

            elif 11 <= player.x <= 14 and 0 <= player.y <= 1:
                zones = 2
                square_ranges = [(5, 14, 0, 9), (11, 14, 0, 14)]

            elif 6 <= player.x <= 10 and 2 <= player.y <= 5:
                zones = 2
                square_ranges = [(5, 14, 0, 9), (0, 14, 2, 5)]

            elif 11 <= player.x <= 14 and 2 <= player.y <= 5:
                zones = 3
                square_ranges = [(5, 14, 0, 9), (0, 14, 2, 5), (11, 14, 0, 14)]

            elif 6 <= player.x <= 10 and 6 <= player.y <= 8:
                zones = 1
                square_ranges = [(5, 14, 0, 9)]

            elif 11 <= player.x <= 14 and 6 <= player.y <= 8:
                zones = 2
                square_ranges = [(5, 14, 0, 9), (11, 14, 0, 14)]

            elif 11 <= player.x <= 14 and 10 <= player.y <= 11:
                zones = 3
                square_ranges = [(5, 14, 9, 14), (11, 14, 0, 14),(0,14,10,11)]

            elif 11 <= player.x <= 14 and 13 <= player.y <= 14:
                zones = 3
                square_ranges = [(5, 14, 9, 14), (11, 14, 0, 14),(0,14,13,14)]

            elif 5 <= player.x <= 10 and 10 <= player.y <= 11:
                zones = 2
                square_ranges = [(5, 14, 9, 14),(0,14,10,11)]

            elif 5<= player.x<=10 and 13 <= player.y <= 14:
                zones=2
                square_ranges = [(5, 14, 9, 14),(0,14,13,14)]

            elif 3 <= player.x <= 4 and 10 <= player.y <= 11:
                zones = 3
                square_ranges = [(0, 14, 10, 11), (3, 4, 0, 11), (0, 4, 7, 11)]

            elif 0 <= player.x <= 2 and 10 <= player.y <= 11:
                zones = 2
                square_ranges = [(0, 14, 10, 11), (0, 4, 7, 11)]

            elif 0 <= player.x <= 2 and 7 <= player.y <= 9:
                zones = 1
                square_ranges = [(0, 4, 7, 11)]

            elif 3 <= player.x <= 4 and 7 <= player.y <= 9:
                zones = 2
                square_ranges = [(3, 4, 0, 11), (0, 4, 7, 11)]

            elif 0 <= player.x <= 4 and 13<= player.y<= 14:
                zones=1
                square_ranges=[(0,14,12,14)]

            elif player.y==12 and 5<=player.x<=14:
                zones=1
                square_ranges=[(0,14,10,14)] 
            elif player.y==6 and 3<=player.x<=4:
                zones=1
                square_ranges = [(0, 5, 0, 14)]

            elif player.y==9 and 11<=player.y<=14:
                zones=1
                square_ranges = [(5, 14, 0, 14)]

            elif player.x==5 and 2<=player.y<=5:
                zones=2
                square_ranges = [(0, 14, 0, 6),(6,14,6,8)]
            
            else:
                square_ranges=[(0,14,0,14)]

            # Check if any enemy is within the visibility zone
            for enemy in self.enemy_units:
                for (min_x, max_x, min_y, max_y) in square_ranges:
                    if min_x <= enemy.x <= max_x and min_y <= enemy.y <= max_y:
                        visible.append(True)  # Enemy is visible in this square
                        break
                else:
                    visible.append(False)  # Enemy is outside all squares

        return visible

    def flip_display(self):
        """Affiche le jeu.
        Change display of game
        """

        # Affiche la grille
        self.screen.fill(BLACK)
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        for block in self.river_blocks:
            block.draw(self.screen)

        for block in self.wall_blocks:
            block.draw(self.screen)


        for grass in self.grass_blocks:
            grass.draw(self.screen)

        burntgrass=GenerateBlocks(ROWS,COLUMNS,'burnt grass',self.burnt_grass)
        burnt_blocks=burntgrass.create_burnt_grass()
        for burnt in burnt_blocks:
            burnt.draw(self.screen)

        # Affiche les bombe/trap
        for bombe in self.bombe_unit:
            bombe.draw(self.screen)

        for bombe in self.bombe_enemy:
            bombe.draw(self.screen)

        for tresore in self.tresore_on_map:
            tresore.draw(self.screen)
        
        # affiche les murs en plus
        for mur in self.wall:
            mur.draw(self.screen)


        # Affiche les unités
        for unit in self.player_units:
            if unit.health<0:
                self.player_units.remove(unit)
            unit.draw(self.screen)

        visible = self.is_enemy_visible()
        enemy_count = len(self.enemy_units)
        for i, enemy_visibility in enumerate(visible):
            enemy_index = i % enemy_count  
            unit = self.enemy_units[enemy_index]
            if enemy_visibility:
                unit.draw(self.screen)

            
        panel_rect = pygame.Rect(WIDTH, 0, PANEL_WIDTH, HEIGHT)
        pygame.draw.rect(self.screen, (50, 50, 50), panel_rect)  
        pygame.draw.rect(self.screen, WHITE, panel_rect, 2)  

        x_offset=WIDTH + 20
        y_offset = 20  

        for unit in self.player_units:
            if unit.is_selected:
                name_text = self.font.render(f"Name: {unit.nom}", True, WHITE)
                self.screen.blit(name_text, (x_offset, y_offset)) 
                y_offset += 30  

                health_text = self.font.render(f"Health: {unit.health}", True, WHITE)
                self.screen.blit(health_text, (x_offset, y_offset)) 
                y_offset += 30
                
                attack_text = self.font.render(f"Attack: {unit.attack_power_base}", True, WHITE)
                self.screen.blit(attack_text, (x_offset, y_offset))  
                y_offset += 30

                defense_text=self.font.render(f"Defense: {unit.defence}",True,WHITE)
                self.screen.blit(defense_text, (x_offset, y_offset))  
                y_offset += 30

                speed_text=self.font.render(f"Speed: {unit.initial_speed}", True, WHITE)
                self.screen.blit(speed_text, (x_offset, y_offset))  
                y_offset += 30

                speed_text=self.font.render(f"Moves Left: {unit.vitesse}", True, WHITE)
                self.screen.blit(speed_text, (x_offset, y_offset))  
                y_offset += 30
                
                self.draw_health_as_hearts(unit, WIDTH + 20, y_offset,"player")
                y_offset += 40  

        for enemy in self.enemy_units:
            name_text = self.font.render(f"Name: {enemy.nom}", True, WHITE)
            self.screen.blit(name_text, (x_offset, y_offset)) 
            y_offset += 30  
            """ 
            health_text = self.font.render(f"Health: {enemy.health}", True, WHITE)
            self.screen.blit(health_text, (x_offset, y_offset))  
            y_offset += 30
            
            attack_text = self.font.render(f"Attack Power: {enemy.attack_power_base}", True, WHITE)
            self.screen.blit(attack_text, (x_offset, y_offset)) 
            y_offset += 30
            """ 
            self.draw_health_as_hearts(enemy, WIDTH + 20, y_offset,"enemy")
            y_offset += 40  

            attack_window_rect = pygame.Rect(WIDTH, HEIGHT - 120, 200, 120)
            pygame.draw.rect(self.screen, (50, 50, 50), attack_window_rect)
            pygame.draw.rect(self.screen, WHITE, attack_window_rect, 2)

            for unit in self.player_units:
                if unit.is_selected:
                    self.show_attack_options(unit, attack_window_rect.left + 10, attack_window_rect.top + 10)

        # Rafraîchit l'écran
        pygame.display.flip()

    def Page_acceuil(self,screen):
        background_image = pygame.image.load("background.png")  
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, HEIGHT))
        title= pygame.font.SysFont('Optima ', 72)
        buttons = pygame.font.SysFont('Optima', 36)
           # Text
        title_text = title.render("Wrath of the Gods", True, WHITE)
        start_text = buttons.render("Commencer", True, BLACK)
        quit_text = buttons.render("Quitter", True, BLACK)
        characters_text=buttons.render("Personnages", True, BLACK)
           # Buttons
        start_button = pygame.Rect(SCREEN_WIDTH // 2-(200//2), HEIGHT // 2-100, 200, 50)
        quit_button = pygame.Rect(SCREEN_WIDTH // 2-(200-350) ,HEIGHT // 2-100, 200, 50)
        characters_button = pygame.Rect(SCREEN_WIDTH // 2-(200+150), HEIGHT // 2-100, 200, 50)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                    if start_button.collidepoint(event.pos):
                        running = False  
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()
                        exit()
                    elif characters_button.collidepoint(event.pos):
                        self.show_characters_page(screen) 
            
            screen.blit(background_image, (0, 0))
            

            
            screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 75))

          
            pygame.draw.rect(screen, WHITE, start_button)
            pygame.draw.rect(screen, WHITE, quit_button)
            pygame.draw.rect(screen, WHITE, characters_button)

            
            screen.blit(start_text, (start_button.x + start_button.width // 2 - start_text.get_width() // 2, start_button.y + 10))
            screen.blit(quit_text, (quit_button.x + quit_button.width // 2 - quit_text.get_width() // 2, quit_button.y + 10))
            screen.blit(characters_text, (characters_button.x + characters_button.width // 2 - characters_text.get_width() // 2, characters_button.y + 10))
            
            pygame.display.flip()
   
    def show_characters_page(self, screen):
        running = True
        background_image = pygame.image.load("background.png")  
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, HEIGHT))
        font = pygame.font.SysFont('Optima', 36)
        subtitle=pygame.font.SysFont('Optima', 20)
        
    
        character_text = font.render("Characters Page", True, WHITE)
        subtitle_text=subtitle.render("Press on Character to view information",True,WHITE)
        back_text = font.render("Back", True, BLACK)

        
        back_button = pygame.Rect(SCREEN_WIDTH - 200 - 20, 20, 200, 50)

        
        character_size = (150, 150)  
        characters = [
            {"image": pygame.image.load("ATHENA.jpeg"), "name": "Athena", "health": 100, "attack": 50, "defense": 30, "rect": pygame.Rect(100, 150, *character_size)},
            {"image": pygame.image.load("poseidon.jpeg"), "name": "Poseidon", "health": 120, "attack": 40, "defense": 40, "rect": pygame.Rect(270, 150, *character_size)},
            {"image": pygame.image.load("zeus.jpeg"), "name": "Zeus", "health": 90, "attack": 70, "defense": 20, "rect": pygame.Rect(440, 150, *character_size)},
            {"image": pygame.image.load("hecate.png"), "name": "Hecate", "health": 90, "attack": 70, "defense": 20, "rect": pygame.Rect(610, 150, *character_size)}
        ]
        
        
        character_info_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, HEIGHT // 2, 400, 200)
        current_character_info = None

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Check if a character image is clicked
                    for character in characters:
                        if character["rect"].collidepoint(event.pos):
                            # Show character info when image is clicked
                            current_character_info = character

                    # Check if back button is clicked
                    if back_button.collidepoint(event.pos):
                        running = False  # Return to the main menu

            screen.blit(background_image, (0, 0))

            
            screen.blit(character_text,(SCREEN_WIDTH // 2 - character_text.get_width() // 2, 75))
            screen.blit(subtitle_text,(SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, 120))
            
            # Draw the character images
            for character in characters:
                character_image = pygame.transform.scale(character["image"], character_size)
                screen.blit(character_image, character["rect"])

            # Draw the back button
            pygame.draw.rect(screen, WHITE, back_button)
            screen.blit(back_text, (back_button.x + back_button.width // 2 - back_text.get_width() // 2, back_button.y + 10))

            if current_character_info:
                pygame.draw.rect(screen, (20, 20, 20), character_info_rect)
                character_info = f"Name: {current_character_info['name']}\nHealth: {current_character_info['health']}\nAttack: {current_character_info['attack']}\nDefense: {current_character_info['defense']}"
                lines = character_info.split("\n")
                y_offset = character_info_rect.top + 20
                for line in lines:
                    info_text = font.render(line, True, WHITE)
                    screen.blit(info_text, (character_info_rect.left + 20, y_offset))
                    y_offset += 30

            pygame.display.flip()


def main():

    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((SCREEN_WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Instanciation du jeu
    game = Game(screen)
    game.Page_acceuil(screen)

    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()
        game.handle_tresore_turn()


if __name__ == "__main__":
    main()
