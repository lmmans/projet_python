import pygame
import random

from enemy import *
from unit import *
from block import *
from oiseau import *
from poisson import *
from defender import * 
from zeus import *


class Game:

    def __init__(self, screen):

        self.screen = screen
        self.player_units = [Oiseau(3, 0, 5,"Athena", 100, 5, 1, 'player', 3, 0),
                             Poisson(1, 0, 3,"Poseidon", 100, 5, 1, 'player', 2, 0),
                             Defender(2, 0, 3,"Hecate", 100, 3, 2, 'player', 1, 0),
                             Assasin(4, 0, 2, "Zeus", 100, 6, 1, 'player', 2, 0)
                             ]

        self.enemy_units = [Defender(3, 11, 3,"Hecate", 100, 50, 5, 'enemy', 1, 0),
                            Assasin(3, 10, 2,"Zeus", 100, 50, 5, 'enemy', 2, 0),
                            Oiseau(3, 9, 5,"Athena", 100, 2, 5, 'enemy', 3, 0)]
        
        self.initial_speed = [player.vitesse for player in self.player_units]

        #Génération de la riviere
        self.generateriver=River(RIVER)
        self.river_blocks = self.generateriver.create()

        #Génération des murs
        self.generatewalls=Wall(WALL)
        self.wall_blocks=self.generatewalls.create()

        #Génération de la pelouse
        self.generategrass=Grass(GRASSUPDATED)
        self.grass_blocks=self.generategrass.create()
        
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
        i = 0
        has_acted = False
        selected_unit.is_selected = True
        for index, selected_unit in enumerate(self.player_units):
            selected_unit.vitesse = self.initial_speed[i]
            i += 1
             #pendant le tour de l'enemy on controlle si il est sur la trap ou no
            if self.bombe_enemy:
            # [:] -> scansion de tous les trap et verification coordonnè avant de la detruire
                for bombe in self.bombe_enemy[:]:
                    bombe.attack_trap(self.player_units, self.burnt_grass, self.bombe_enemy)
                    self.flip_display()


            # Tant que l'unité n'a pas terminé son tour


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
                            bonus_applied = Tresore.compare_position_tresore(self, self.tresore_on_map, selected_unit, self.initial_speed, index)
                        # "bonus_applied" return True si la Trap a été touché
                            if bonus_applied:
                                has_acted = True
                                selected_unit.is_selected = False
                                self.flip_display()
                            else:
                                has_acted = False
                    #ATTAQUES
                        #attaque "q" (attque multiple base pour tous)
                        if event.key == pygame.K_q:
                            selected_unit.attack1(self.wall, self.enemy_units)
                            #changer l'unité apre l'attaque
                            has_acted = True
                            selected_unit.is_selected = False

                        # attaque "s" (Hecate -> defene +2, Zeus -> attaque distace 1)                                         
                        elif event.key == pygame.K_s:
                            if selected_unit.nom == "Hecate":
                                selected_unit.attack2()
                                has_acted = True
                                selected_unit.is_selected = False
                            elif selected_unit. nom == "Zeus":
                                selected_unit.attack2(self.enemy_units)
                                has_acted = True
                                selected_unit.is_selected = False
                            else:
                                has_acted = False

                        # attaque "d" (Hecate -> health +5 allies, Athena -> creation mu, Poiseidon -> creation shark)
                        elif event.key == pygame.K_d:
                            if selected_unit.nom == "Athena":
                                # lititation creation mur a 4 fois
                                if len (self.wall) <= 3:
                                    new_wall = Mur(selected_unit.x, selected_unit.y)
                                    self.wall.append(new_wall)
                                    has_acted = True
                                    selected_unit.is_selected = False 
                                else:
                                    has_acted = False

                            if selected_unit.nom == "Poseidon":
                                if len (self.player_units) <= 6:
                                    new_shark = Shark(selected_unit.x +1, selected_unit.y + 1, 4, "Shark", 20, 7, 1, 'player', 1, 0)
                                    self.player_units.append(new_shark)
                                    self.initial_speed.append(new_shark.vitesse)
                                    has_acted = True
                                    selected_unit.is_selected = False
                                else:
                                    has_acted = False
                            # boucle pour tous les allies sauf lui
                            if selected_unit.nom == "Hecate":
                                selected_unit.attack3(self.player_units)  
                                has_acted = True
                                selected_unit.is_selected = False

                            if selected_unit.nom == "Zeus":
                                selected_unit.teleportation()

                                has_acted=True
                                selected_unit.is_selected= False

                        # attque "f" (Athena, Poseidon -> bombe/trap, Hecate -> + 4 attack power, Zeus -> foudre)
                        elif event.key == pygame.K_f:
                            if selected_unit.nom == "Athena" or selected_unit.nom == "Poseidon":
                                # creation unité dans la liste ""self.bombe_unit"
                                new_bombe = Bombe(selected_unit.x, selected_unit.y, 2,"player")
                                self.bombe_unit.append(new_bombe)
                                self.flip_display()
                                self.handle_bombe_turn(new_bombe,selected_unit)
                                        
                            elif selected_unit.nom == "Hecate":
                                selected_unit.power_allies(self.player_units)

                            elif selected_unit.nom == "Zeus":
                                selected_unit.attack_foudre(self.enemy_units) 
                            has_acted = True
                            selected_unit.is_selected = False

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
                        if not has_acted: 
                            bombe_unit.move(dx, dy)
                            self.flip_display()

                # touche SPACE pour attaquer ou installer la bombe
                        if event.key == pygame.K_SPACE:

                # Zeus -> lance la bombe, la bombe est detruit apres l'attaque
                # aussi si la cible n'est pas touchè
                            if selected_unit.nom == "Poseidon":
                                bombe_unit.attack_bombe(self.enemy_units, self.burnt_grass)
                                self.bombe_unit.remove(bombe_unit)  
                                self.flip_display()
                                return 
                    
                            elif selected_unit.nom == "Athena":
                                bombe_unit.attack_trap(self.enemy_units, self.burnt_grass, self.bombe_unit)
                                self.flip_display()
                                return

    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""
        for enemy in self.enemy_units:
            ## j'ai essaie de remetre ici l'attaque de Zeus me ne marche pas
            enemy.health -= enemy.additional_damage
            

            targets_in_range = [
            player for player in self.player_units
            if abs(enemy.x - player.x) <= enemy.distance_attack and abs(enemy.y - player.y) <= enemy.distance_attack
            ]

            if targets_in_range:
                # If targets are in range, choose the closest one
                target = min(
                    targets_in_range,
                    key=lambda player: abs(enemy.x - player.x) + abs(enemy.y - player.y)
                )
            else:
                # If no targets in range, select a random target
                target = random.choice(self.player_units)
            
            if enemy.nom=="Athena":
                move_not_possible=RIVER
            elif enemy.nom=="Poseidon":
                move_not_possible=WALL
            else: 
                move_not_possible=DONOTGO
            
            enemy_attacks=Enemy(enemy, target, move_not_possible,self.enemy_units,self.player_units,self.wall)
            dx,dy=enemy_attacks.move_towards_target()
            

                 
            #pendant le tour de l'enemy on controlle si il est sur la trap ou no
            if self.bombe_unit:
            # [:] -> scansion de tous les trap et verification coordonnè avant de la detruire
                for bombe in self.bombe_unit[:]:
                    bombe.attack_trap(self.enemy_units, self.burnt_grass, self.bombe_unit)
                    self.flip_display()

            attack_methods =enemy.attack_methodes_enemies
            chosen_attack = random.choice(attack_methods)

            if chosen_attack!="Teleportation":
                enemy.move(dx,dy, self.wall)


            enemy_attacks.attack_IA(chosen_attack,self.bombe_enemy,self.burnt_grass)
            self.flip_display()
            continue
    
    def handle_tresore_turn(self): 
        Tresore.spawn_tresore(self, self.tresore_on_map)
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
                square_ranges = [(0, 5, 0, 6)]

            elif 0 <= player.x <= 2 and 2 <= player.y <= 5:
                square_ranges = [(0, 5, 0, 6), (0, 14, 2, 5)]

            elif 3 <= player.x <= 4 and 2 <= player.y <= 5:
                square_ranges = [(0, 5, 0, 6), (0, 14, 2, 5), (3, 5, 0, 14)]

            elif 3 <= player.x <= 4 and 0 <= player.y <= 1:
                square_ranges = [(0, 5, 0, 6), (3, 5, 0, 14)]

            elif 6 <= player.x <= 10 and 0 <= player.y <= 1:
                square_ranges = [(5, 14, 0, 9)]

            elif 11 <= player.x <= 14 and 0 <= player.y <= 1:
                square_ranges = [(5, 14, 0, 9), (11, 14, 0, 14)]

            elif 6 <= player.x <= 10 and 2 <= player.y <= 5:
                square_ranges = [(5, 14, 0, 9), (0, 14, 2, 5)]

            elif 11 <= player.x <= 14 and 2 <= player.y <= 5:
                square_ranges = [(5, 14, 0, 9), (0, 14, 2, 5), (11, 14, 0, 14)]

            elif 6 <= player.x <= 10 and 6 <= player.y <= 8:
                square_ranges = [(5, 14, 0, 9)]

            elif 11 <= player.x <= 14 and 6 <= player.y <= 8:
                square_ranges = [(5, 14, 0, 9), (11, 14, 0, 14)]

            elif 11 <= player.x <= 14 and 10 <= player.y <= 11:
                square_ranges = [(5, 14, 9, 14), (11, 14, 0, 14),(0,14,10,11)]

            elif 11 <= player.x <= 14 and 13 <= player.y <= 14:
                square_ranges = [(5, 14, 9, 14), (11, 14, 0, 14),(0,14,13,14)]

            elif 5 <= player.x <= 10 and 10 <= player.y <= 11:
                square_ranges = [(5, 14, 9, 14),(0,14,10,11)]

            elif 5<= player.x<=10 and 13 <= player.y <= 14:
                square_ranges = [(5, 14, 9, 14),(0,14,13,14)]

            elif 3 <= player.x <= 4 and 10 <= player.y <= 11:
                square_ranges = [(0, 14, 10, 11), (3, 4, 0, 11), (0, 4, 7, 11)]

            elif 0 <= player.x <= 2 and 10 <= player.y <= 11:
                square_ranges = [(0, 14, 10, 11), (0, 4, 7, 11)]

            elif 0 <= player.x <= 2 and 7 <= player.y <= 9:
                square_ranges = [(0, 4, 7, 11)]

            elif 3 <= player.x <= 4 and 7 <= player.y <= 9:
                square_ranges = [(3, 4, 0, 11), (0, 4, 7, 11)]

            elif 0 <= player.x <= 4 and 13<= player.y<= 14:
                square_ranges=[(0,14,12,14)]

            elif player.y==12 and 5<=player.x<=14:
                square_ranges=[(0,14,10,14)] 

            elif player.y==6 and 3<=player.x<=4:
                square_ranges = [(0, 5, 0, 14)]

            elif player.y==9 and 11<=player.y<=14:
                square_ranges = [(5, 14, 0, 14)]

            elif player.x==5 and 2<=player.y<=5:
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
    
    def fin_jeu(self,gamestatus):
        if gamestatus:
            game_state="You Win"
            Color=GREEN
        else:
            game_state="You Lose"
            Color=RED
        
        self.screen.fill(BLACK)
        font = pygame.font.SysFont('Optima', 72)
        text = font.render(game_state, True, Color)
        buttons = pygame.font.SysFont('Optima', 36)
           
        
        quit_text = buttons.render("Quit", True, BLACK)
        
           # Buttons
        quit_button = pygame.Rect((SCREEN_WIDTH-200)// 2 ,(HEIGHT-50) // 2, 200, 50)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                    if quit_button.collidepoint(event.pos):
                        pygame.quit()
                        exit() 
            
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 75))
            pygame.draw.rect(self.screen, WHITE, quit_button)
            self.screen.blit(quit_text, (quit_button.x + quit_button.width // 2 - quit_text.get_width() // 2, quit_button.y + 10))
            pygame.display.flip()



    def flip_display(self):
        """Affiche le jeu.
        Change display of game
        """
        if len(self.player_units)==0:
            status=False
            self.fin_jeu(status)
        elif len(self.enemy_units)==0:
            status=True
            self.fin_jeu(status)


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

        burntgrass=BurntGrass(self.burnt_grass)
        burnt_blocks=burntgrass.create()
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
