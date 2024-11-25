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

#essay
class AttaqueSpeciale:
    def __init__(self, type_attaque_speciale):
        self.type_attaque_speciale = type_attaque_speciale

    def effet_special(self):
        if self.type_attaque_speciale == "Ailes":
            return {"attaque": 5}   #Bonus de vitesse pour "Ailes"
        elif self.type_attaque_speciale == "Bombe":
            return #{"attaque": 10}   Bonus d'attaque pour "Bombe"
        elif self.type_attaque_speciale == "Soin":
            return #{"points_de_vie": 20}   Restauration des PV
        elif self.type_attaque_speciale == "Poison":
            return #{"attaque": -3, "defense": -3}   Malus pour l'ennemi
        else:
            return {}

#essay
class Equipement:
    def __init__(self, nom, bonus_statistiques):
        self.nom = nom
        self.bonus_statistiques = bonus_statistiques

#essay
class Statistique:
    def __init__(self, points_de_vie, attaque, attaque_speciale, prob_attaque, defense, prob_defense, vitesse):
        self.points_de_vie = points_de_vie
        self.attaque = attaque
        self.attaque_speciale = attaque_speciale
        self.prob_attaque = prob_attaque
        self.defense = defense
        self.prob_defense = prob_defense
        self.vitesse = vitesse

        # Application des effets de l'attaque spéciale
        effets = AttaqueSpeciale(self.attaque_speciale).effet_special()
        for stat, valeur in effets.items():
            if hasattr(self, stat):
                setattr(self, stat, getattr(self, stat) + valeur)

    def __str__(self):
        return (f"Points de vie: {self.points_de_vie}, Attaque: {self.attaque}, "
                f"Attaque spéciale: {self.attaque_speciale}, Vitesse: {self.vitesse}, "
                f"Défense: {self.defense}")

#esssay    
class Unit:
    def __init__(self, x, y, nom, equipe, statistique):
        self.x = x
        self.y = y
        self.nom = nom
        self.equipe = equipe  # 'joueur' ou 'ennemi'
        self.statistique = statistique
        self.is_selected = False
        self.equipement_actuel = None
        self.inventaire = [] #Inventory 

    def equiper(self, equipement):
        # Équipe le nouvel équipement
        if equipement in self.inventaire:
            self.equipement_actuel = equipement
            self.appliquer_bonus(equipement)

    def appliquer_bonus(self, equipement):
        for stat, bonus in equipement.bonus_statistiques.items():
            if hasattr(self.statistique, stat):
                setattr(self.statistique, stat, getattr(self.statistique, stat) + bonus)

    def ajouter_equipement(self, equipement):
        self.inventaire.append(equipement)

    def __str__(self):
        return f"Nom: {self.nom}, Équipe: {self.equipe}, \nStatistiques:\n {self.statistique}"

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
        color = BLUE if self.equipe == 'player' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
                           2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
        

""" 

# Création d'équipements
epee = Equipement("Epee", bonus_statistiques={"attaque": 8})
armure = Equipement("Armure", bonus_statistiques={"defense": 5})
chaussures = Equipement("Chaussures", bonus_statistiques={"vitesse": 2})


#--Création d'une unité
statistiques = Statistique(50, 15, "Ailes", 4, 10, 5, 7)
oiseau = Unit(3, 4, "Oiseau", "Joueur", statistique=statistiques)

print("Statistiques initiales de l'unité :")
print(oiseau)

#--Ajout et équipement d'un équipement
oiseau.ajouter_equipement(chaussures)
oiseau.equiper(chaussures)

print("\nStatistiques après avoir équipé l'accessoire :")
print(oiseau)
"""
