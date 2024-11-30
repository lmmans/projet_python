import pygame
import random

from unit import *
from block import *


class Game:
    """
    Classe pour représenter le jeu.

    ...
    Attributs
    ---------
    screen: pygame.Surface
        La surface de la fenêtre du jeu.
    player_units : list[Unit]
        La liste des unités du joueur.
    enemy_units : list[Unit]
        La liste des unités de l'adversaire.
    """

    def __init__(self, screen):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        self.athena_statistique = Statistique(100, 15, "Ailes", 4, 10, 5, 7)
        self.poseidon_statistique=Statistique(100, 15, "Poisson", 4, 10, 5, 7)
        self.zeus_statistique=Statistique(100, 15, "Bombe", 4, 10, 5, 7)
        self.hecate_statistique=Statistique(100, 15, "Bombe", 4, 10, 5, 7)
        self.screen = screen
        self.player_units = [Unit("Poseidon",0, 0, 10, 2, 'player',self.athena_statistique),
                             Unit("Athena",1, 0, 10, 2, 'player',self.poseidon_statistique)]

        self.enemy_units = [Unit("Zeus",6, 6, 8, 1, 'enemy',self.zeus_statistique),
                            Unit("Hecate",7, 6, 8, 1, 'enemy',self.zeus_statistique)]
        

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

                        selected_unit.move(dx, dy)
                        self.flip_display()

                        # Attaque (touche espace) met fin au tour
                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    selected_unit.attack(enemy)
                                    if enemy.health <= 0:
                                        self.enemy_units.remove(enemy)

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
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
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

            attack_text = self.font.render(f"Attack: {unit.attack_power}", True, WHITE)
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
