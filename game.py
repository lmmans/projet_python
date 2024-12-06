import pygame
import random

from unit import *
from block import *
from oiseau import *
from poisson import *


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
        self.player_units = [Oiseau(0, 0, 4,"Athena", 10, 2, 5, 'player', 3,0),
                             Poisson(1, 0, 1,"Poseidon", 10, 8, 5, 'player', 3,0)]

        self.enemy_units = [Defender(6, 6, 4,"b", 20, 8, 5, 'enemy', 1,0),
                            Assasin(7, 6, 4,"b", 20, 8, 5, 'enemy', 1,0)]
        

        #Génération de la riviere
        self.generateriver=GenerateBlocks(ROWS,COLUMNS,'river')
        self.river_blocks = self.generateriver.create_river()

        #Génération des murs
        self.generatewalls=GenerateBlocks(ROWS,COLUMNS,'wall')
        self.wall_blocks=self.generatewalls.create_wall()

        #Génération de la pelouse
        self.generategrass=GenerateBlocks(ROWS,COLUMNS,'grass')
        self.grass_blocks=self.generategrass.create_grass()
        
        self.font = pygame.font.SysFont('Arial', 24)

    def handle_player_turn(self):
        """Tour du joueur"""
        for selected_unit in self.player_units:
            if selected_unit.nom == "Athena":
                ###essaier de le faire bouger 2 pas a la fois
                selected_unit.vitesse = 4 
            if selected_unit.nom == "Poseidon":
                selected_unit.vitesse = 3

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

                    #attaques
                        if event.key == pygame.K_a:
                            for enemy in self.enemy_units:
                                # Controlla se il nemico è entro il raggio di attacco
                                if abs(selected_unit.x - enemy.x) <= selected_unit.distance_attack and abs(selected_unit.y - enemy.y) <= selected_unit.distance_attack:
                                    selected_unit.attack1(enemy)
                                    if enemy.health <= 0:
                                        self.enemy_units.remove(enemy)

                            has_acted = True
                            selected_unit.is_selected = False
                                    # Mostra opzioni d'attacco
                                    
                        elif event.key == pygame.K_s:
                            pass
                            #selected_unit.attack2(enemy)  # Esegue il secondo tipo di attacco
                        elif event.key == pygame.K_d:
                            pass
                            #selected_unit.attack3(enemy)  # Esegue il terzo tipo di attacco

                        if event.key == pygame.K_SPACE:
                            has_acted = True
                            selected_unit.is_selected = False


    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""
        for enemy in self.enemy_units:

            # Déplacement aléatoire
            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy)

            # Attaque si possible
            if abs(enemy.x - target.x) <= enemy.distance_attack and abs(enemy.y - target.y) <= enemy.distance_attack:
                enemy.attack1(target)
                if target.health <= 0:
                    self.player_units.remove(target)


    def draw_health_as_hearts(self, unit, x_offset, y_offset):
        max_health = 100  
        heart_size = 20  
        num_hearts = 10  

        filled_hearts = (unit.health / max_health) * num_hearts
        full_hearts = int(filled_hearts)  
        empty_hearts = num_hearts - full_hearts 

        
        for i in range(full_hearts):
            heart_rect = pygame.Rect(x_offset + i * (heart_size + 5), y_offset, heart_size, heart_size)
            pygame.draw.rect(self.screen, (255, 0, 0), heart_rect)  

        # Dessin des cœurs vides
        for i in range(full_hearts, num_hearts):
            heart_rect = pygame.Rect(x_offset + i * (heart_size + 5), y_offset, heart_size, heart_size)
            pygame.draw.rect(self.screen, (100, 100, 100), heart_rect) 


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
        

        # Affiche les unités
        for unit in self.player_units + self.enemy_units:
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

            health_text = self.font.render(f"Health: {unit.health}", True, WHITE)
            self.screen.blit(health_text, (x_offset, y_offset)) 
            y_offset += 30

            attack_text = self.font.render(f"Attack: {unit.attack_power_base}", True, WHITE)
            self.screen.blit(attack_text, (x_offset, y_offset))  
            y_offset += 30
            self.draw_health_as_hearts(unit, WIDTH + 20, y_offset)
            y_offset += 40  

        for enemy in self.enemy_units:
            name_text = self.font.render(f"Name: {enemy.nom}", True, WHITE)
            self.screen.blit(name_text, (x_offset, y_offset)) 
            y_offset += 30  

            health_text = self.font.render(f"Health: {enemy.health}", True, WHITE)
            self.screen.blit(health_text, (x_offset, y_offset))  
            y_offset += 30

            attack_text = self.font.render(f"Attack Power: {enemy.attack_power_base}", True, WHITE)
            self.screen.blit(attack_text, (x_offset, y_offset)) 
            y_offset += 30
            self.draw_health_as_hearts(enemy, WIDTH + 20, y_offset)
            y_offset += 40  

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
        start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, HEIGHT // 4, 200, 50)
        quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, HEIGHT // 4 + 80, 200, 50)
        characters_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, HEIGHT // 4 + 160, 200, 50)

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
            

            
            screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

          
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
            {"image": pygame.image.load("ATHENA.jpeg"), "name": "Athena", "health": 100, "attack": 50, "defense": 30, "rect": pygame.Rect(100, 200, *character_size)},
            {"image": pygame.image.load("poseidon.jpeg"), "name": "Poseidon", "health": 120, "attack": 40, "defense": 40, "rect": pygame.Rect(270, 200, *character_size)},
            {"image": pygame.image.load("zeus.jpeg"), "name": "Zeus", "health": 90, "attack": 70, "defense": 20, "rect": pygame.Rect(440, 200, *character_size)},
            {"image": pygame.image.load("hecate.png"), "name": "Hecate", "health": 90, "attack": 70, "defense": 20, "rect": pygame.Rect(610, 200, *character_size)}
        ]
        
        
        character_info_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, HEIGHT // 2 - 50, 400, 200)
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

            
            screen.blit(character_text,(SCREEN_WIDTH // 2 - character_text.get_width() // 2, 100))
            screen.blit(subtitle_text,(SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, 150))
            
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
