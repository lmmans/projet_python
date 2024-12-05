import pygame
import random

from unit import *
from block import *
from oiseau1 import *
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

        filled_hearts = (unit.statistique.points_de_vie / max_health) * num_hearts
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

            attack_text = self.font.render(f"Attack Power: {enemy.attack_power}", True, WHITE)
            self.screen.blit(attack_text, (x_offset, y_offset)) 
            y_offset += 30
            self.draw_health_as_hearts(enemy, WIDTH + 20, y_offset)
            y_offset += 40  

        # Rafraîchit l'écran
        pygame.display.flip()


def main():

    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((SCREEN_WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Instanciation du jeu
    game = Game(screen)

    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()


if __name__ == "__main__":
    main()
