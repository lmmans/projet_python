import pygame
import random
from block import *



# Constantes
GRID_SIZE = 15
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
RIVER=[(0,2),(1,2),(0,3),(1,3),(2,3),(3,3),(2,4),(3,4),(4,4),(5,4),(11,0),(11,1),(11,2),(11,3),(11,4),
                               (10,1),(12,1),(9,2),(10,2),(12,2),(13,2),(10,3),(12,3),
                               ]
WALL=[(5,0),(5,1),(5,6),(5,7),(5,8),(5,9),(6,9),(7,9),(8,9),(9,9),(10,9),(0,6),(1,6),(2,6)]
DONOTGO=set(RIVER+WALL) # ARRETER LES UNITES DE PARTIR DANS CES BLOCKS

PANEL_WIDTH = 300  
SCREEN_WIDTH = WIDTH + PANEL_WIDTH   # Pour afficher les statistiques


#essay
class AttaqueSpeciale:
    def __init__(self, type_attaque_speciale):
        self.type_attaque_speciale = type_attaque_speciale

    def effet_special(self):
        if self.type_attaque_speciale == "Ailes":
            return {"attaque": 5}   #Bonus de vitesse pour "Ailes"
        elif self.type_attaque_speciale == "Bombe":
            return {"attaque": 10}   #Bonus d'attaque pour "Bombe"
        elif self.type_attaque_speciale == "Soin":
            return {"points_de_vie": 20}   #Restauration des PV
        elif self.type_attaque_speciale == "Poison":
            return {"attaque": -3, "defense": -3}   #Malus pour l'ennemi
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

class Characters:
    def __init__(self):
        pass

    def oiseau(self):
        statistiques=Statistique(50, 15, "Ailes", 4, 10, 5, 7)
        photo=pygame.image.load("ATHENA.jpeg")
        return photo,statistiques
    
    def poisson(self):
        statistiques=Statistique(50,15,"Poisson",4,10,5,7)
        photo=pygame.image.load("poseidon.jpeg")
        return photo,statistiques
    
    def defenseur(self):
        statistique=Statistique(50,15,"Soin",4,10,5,7)
        photo=pygame.image.load("hecate.png")
        return photo, statistique

    def attaqueur(self):
        statistiques=Statistique(50,15,"Bombe",4,10,5,7)
        photo=pygame.image.load("zeus.jpeg")
        return photo,statistiques

class Unit():
    """
    Classe pour représenter une unité.

    ...
    Attributs
    ---------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    health : int
        La santé de l'unité.
    attack_power : int
        La puissance d'attaque de l'unité.
    team : str
        L'équipe de l'unité ('player' ou 'enemy').
    is_selected : bool
        Si l'unité est sélectionnée ou non.

    Méthodes
    --------
    move(dx, dy)
        Déplace l'unité de dx, dy.
    attack(target)
        Attaque une unité cible.
    draw(screen)
        Dessine l'unité sur la grille.
    """

    def __init__(self,nom, x, y, health, attack_power, team,statistique):
        """
        Construit une unité avec une position, une santé, une puissance d'attaque et une équipe.

        Paramètres
        ----------
        x : int
            La position x de l'unité sur la grille.
        y : int
            La position y de l'unité sur la grille.
        health : int
            La santé de l'unité.
        attack_power : int
            La puissance d'attaque de l'unité.
        team : str
            L'équipe de l'unité ('player' ou 'enemy').
        """
        self.x = x
        self.y = y
        self.nom = nom
        self.health = health
        self.attack_power = attack_power
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False
        self.statistique=statistique

    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        
        new_x = self.x + dx
        new_y = self.y + dy

        if (0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE 
                and (new_x, new_y) not in DONOTGO):
            self.x = new_x
            self.y = new_y
        

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        if self.nom=="Athena":
            Athena=Characters()
            photo,statistiques=Athena.oiseau()
        elif self.nom=="Poseidon":
            Poseidon=Characters()
            photo,statistiques=Poseidon.poisson()
        elif self.nom=="Zeus":
            Zeus=Characters()
            photo,statistiques=Zeus.attaqueur()
        elif self.nom=="Hecate":
            Hecate=Characters()
            photo,statistiques=Hecate.defenseur()

        scaled_image = pygame.transform.scale(photo, (CELL_SIZE,CELL_SIZE))
        screen.blit(scaled_image, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        

        """ 
        color = BLUE if self.team == 'player' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
                           2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
        """

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
