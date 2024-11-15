import pygame
import random

# Constantes
GRID_SIZE = 8
CELL_SIZE = 60
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
COLUMNS=WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Stats:
    """
    Classe pour les statistiques unité
    """
    def __init__(self, point_de_vie, prob_attaque, prob_defense, vitesse):
        self.point_de_vie = point_de_vie
        self.prob_attaque = prob_attaque
        self.prob_defense = prob_defense
        self.vitesse = vitesse

class Equipment:
    """
    Classe por arme ou autre
    """
    def __init__(self, weapon=None, armor=None, accessory=None):
        self.weapon = weapon
        self.armor = armor
        self.accessory = accessory

    def get_bonus(self):
        """
        Prototipe pour ajouter bonus a mettre ici ou directement dans la class Unit (comment pour example la vitesse pour le poisson)
        """
        bonus = {"attack": 0, "defense": 0}
        if self.weapon:
            bonus["attack"] += self.weapon.get("attack", 0)
        if self.armor:
            bonus["defense"] += self.armor.get("defense", 0)
        if self.accessory:
            bonus["mana"] += self.accessory.get("mana", 0)
        return bonus
    
class Unit:
    """
    Classe pour représenter une unité.
    """
    def __init__(self, x, y, name, team, attaque, attaque_special, defence, stats, image_path=None):
        self.x = x
        self.y = y
        self.name = name
        self.team = team  # 'player' o 'enemy'
        self.attaque = attaque
        self.attaque_special = attaque_special
        self.defence = defence
        self.stats = stats
        self.is_selected = False
        # pour ajouter image
        self.image = pygame.image.load(image_path) if image_path else None 

    """ pas encore implementè

    Méthodes
    --------
    move(dx, dy)
        Déplace l'unité de dx, dy.
    attack(target)
        Attaque une unité cible.
    draw(screen)
        Dessine l'unité sur la grille.
    """

    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            self.x += dx
            self.y += dy

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        color = BLUE if self.team == 'player' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
                           2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
