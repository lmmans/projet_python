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
                             Poisson(1, 0, 1,"Poseidon", 80, 8, 5, 'player', 3, 0),
                             Defender(2, 0, 4,"Hecate", 80, 1, 5, 'enemy', 2, 0)
                             ]

        self.enemy_units = [Defender(3, 12, 4,"Hecate", 100, 8, 5, 'enemy', 1, 0),
                            Assasin(13, 14, 4,"Zeus", 100, 8, 5, 'enemy', 1, 0)]
        
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

    def show_attack_options(self, selected_unit,x,y):
        attack_text = [
            f"Player: {selected_unit.nom}",
            f"A: {selected_unit.attack1_name}",
            f"S: {selected_unit.attack2_name}",
            f"D: {selected_unit.attack3_name}",
            f"F: {selected_unit.attack4_name}",
        ]
     
        for i, line in enumerate(attack_text):
            text_surface = self.font.render(line, True, WHITE)
            self.screen.blit(text_surface, (x, y + i * 20))

    def handle_player_turn(self):
        """Tour du joueur"""
        #print(self.initial_speed)
        #print("coucou")
        i = 0
        for selected_unit in self.player_units:
            
            selected_unit.vitesse = self.initial_speed[i]
            print(self.initial_speed[i])
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
                            selected_unit.move(dx, dy)
                            self.flip_display()

                    #ATTAQUES
                        #attaque "a" (attque multiple base pour tous)
                        if event.key == pygame.K_a:
                            for enemy in self.enemy_units:
                                # boucle pou attaquer tout les enemy
                                if abs(selected_unit.x - enemy.x) <= selected_unit.distance_attack and abs(selected_unit.y - enemy.y) <= selected_unit.distance_attack:
                                    selected_unit.attack1(enemy)
                                    if enemy.health <= 0:
                                        self.enemy_units.remove(enemy)
                            #changer l'unité apre l'attaque
                            has_acted = True
                            selected_unit.is_selected = False

                        # attaque "s" (Hecate -> defene +2)                                         
                        elif event.key == pygame.K_s:
                            selected_unit.attack2()
                            has_acted = True
                            selected_unit.is_selected = False

                        # attaque "d" (Hecate -> health +5 allies)
                        elif event.key == pygame.K_d:
                            # boucle pour tous les allies...
                            for unit in (self.player_units):
                                # ...sauf lui
                                if unit != selected_unit:
                                    if abs(selected_unit.x - unit.x) <= selected_unit.distance_attack and abs(selected_unit.y - unit.y) <= selected_unit.distance_attack:
                                        selected_unit.attack3(unit)  
                            has_acted = True
                            selected_unit.is_selected = False

                        # attque "f" (Athena, Zeus -> attaque siblé)
                        elif event.key == pygame.K_f:
                            if selected_unit.nom == "Athena" or selected_unit.nom == "Hecate":
                                # creation unité dans la liste ""self.bombe_unit"
                                new_bombe = Bombe(selected_unit.x, selected_unit.y, 2)
                                self.bombe_unit.append(new_bombe)
                                #self.bombe_unit.draw(self.screen)
                                self.flip_display()
                                self.handle_bombe_turn(new_bombe,selected_unit)
                                        
                            elif selected_unit.nom == "Poseidon" or selected_unit.nom == "Zeus":
                                pass
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
                        if not has_acted:  # Permette di muovere solo finché non è stata fatta un'azione
                            bombe_unit.move(dx, dy)
                            self.flip_display()

                # touche SPACE pour attaquer ou installer la bombe
                        if event.key == pygame.K_SPACE:

                # Zeus -> lance la bombe, la bombe est detruit apres l'attaque
                # aussi si la cible n'est pas touchè
                                if selected_unit.nom == "Hecate":
                                    for enemy in self.enemy_units:
                                        if abs(enemy.x - bombe_unit.x) <= bombe_unit.distance_attack and abs(enemy.y - bombe_unit.y) <= bombe_unit.distance_attack: 
                                            bombe_unit.attack_bombe(enemy)
                                        self.bombe_unit.remove(bombe_unit)  # Rimuove correttamente la bomba dalla lista
                                        self.flip_display()
                                        return 
                                    if not enemy:
                                            self.bombe_unit.remove(bombe_unit)  # Rimuove correttamente la bomba dalla lista
                                            self.flip_display()
                                            return
                                    
                # Athena -> installe la bombe (trap) au sol
                # trap detrite seulement si l'enemy la touche                    
                                elif selected_unit.nom == "Athena":
                                    for enemy in self.enemy_units:
                                        if enemy.x == bombe_unit.x and enemy.y == bombe_unit.y:
                                            bombe_unit.attack_bombe(enemy)
                                            self.bombe_unit.remove(bombe_unit)#bombe_unit = None  # Rimuove la bomba dopo l'attacco
                                            self.flip_display()
                                        else:
                                            self.flip_display()
                                            return
        

    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""
        for enemy in self.enemy_units:

            # Déplacement aléatoire
            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy)
            #pendant le tour de l'enemy on controlle si il est sur la trap ou no
            if self.bombe_unit:
            # [:] -> scansion de tous les trap et verification coordonnè avant de la detruire
                for bombe in self.bombe_unit[:]:
                    if enemy.x == bombe.x and enemy.y == bombe.y:
                        bombe.attack_bombe(enemy)
                        self.bombe_unit.remove(bombe)
                        self.flip_display()
                    else:
                        self.flip_display()

            # Attaque si possible
            if abs(enemy.x - target.x) <= enemy.distance_attack and abs(enemy.y - target.y) <= enemy.distance_attack:
                enemy.attack1(target)
                if target.health <= 0:
                    self.player_units.remove(target)


    def draw_health_as_hearts(self, unit, x_offset, y_offset,team):
        max_health = 100  
        heart_size = 20  
        num_hearts = 10  

        filled_hearts = (unit.health / max_health) * num_hearts
        full_hearts = int(filled_hearts)  
        empty_hearts = num_hearts - full_hearts 
        if team=="enemy":
            heart_color=GREEN
        elif team =="player":
            heart_color=RED
        
        for i in range(full_hearts):
            heart_rect = pygame.Rect(x_offset + i * (heart_size + 5), y_offset, heart_size, heart_size)
            pygame.draw.rect(self.screen, heart_color, heart_rect)  

        # Dessin des cœurs vides
        for i in range(full_hearts, num_hearts):
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

            elif 11 <= player.x <= 14 and 10 <= player.y <= 14:
                zones = 2
                square_ranges = [(0, 14, 9, 14), (11, 14, 0, 14)]

            elif 5 <= player.x <= 10 and 10 <= player.y <= 14:
                zones = 1
                square_ranges = [(0, 14, 9, 14)]

            elif 3 <= player.x <= 4 and 10 <= player.y <= 14:
                zones = 3
                square_ranges = [(0, 14, 10, 14), (3, 4, 0, 14), (0, 4, 7, 14)]

            elif 0 <= player.x <= 2 and 10 <= player.y <= 14:
                zones = 2
                square_ranges = [(0, 14, 10, 14), (0, 4, 7, 14)]

            elif 0 <= player.x <= 2 and 7 <= player.y <= 9:
                zones = 2
                square_ranges = [(0, 4, 7, 14)]

            elif 3 <= player.x <= 4 and 7 <= player.y <= 9:
                zones = 2
                square_ranges = [(3, 4, 0, 14), (0, 4, 7, 14)]

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

        # Affiche les bombe/trap
        for bombe in self.bombe_unit:
            bombe.draw(self.screen)
        

        # Affiche les unités
        for unit in self.player_units:
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
            name_text = self.font.render(f"Name: {unit.nom}", True, WHITE)
            self.screen.blit(name_text, (x_offset, y_offset)) 
            y_offset += 30  
            """ 
            health_text = self.font.render(f"Health: {unit.health}", True, WHITE)
            self.screen.blit(health_text, (x_offset, y_offset)) 
            y_offset += 30
            
            attack_text = self.font.render(f"Attack: {unit.attack_power_base}", True, WHITE)
            self.screen.blit(attack_text, (x_offset, y_offset))  
            y_offset += 30
            """ 
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


if __name__ == "__main__":
    main()
