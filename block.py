import pygame
import random
from unit import*


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

BLOCKTYPES=['river','wall',"grass"]
BLOCKIMAGE={
    'river': pygame.image.load("water.png"),
    'wall': pygame.image.load("wall.png"), 
    'grass': pygame.image.load("grass.png")
}

class BLOCK:
    def __init__(self, x, y, block_type):
        self.x = x
        self.y = y
        self.block_type = block_type
        self.image = BLOCKIMAGE[block_type]

    def draw(self, screen):
        
        scaled_image = pygame.transform.scale(self.image, (CELL_SIZE,CELL_SIZE))
        screen.blit(scaled_image, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        


class GenerateBlocks:
    def __init__(self, lignes, colonnes,block_type):
        self.lignes = lignes
        self.colonnes = colonnes
        self.image = BLOCKIMAGE[block_type]
    
        self.rivercoordinates= RIVER
        self.wallcoordinates= WALL
        self.grasscoordinates= [(i,j) for i in range(ROWS) for j in range(COLUMNS)]
        self.grasscoordinates2=[x for x in self.grasscoordinates if x not in set(self.wallcoordinates)]
        self.grasscoordinatesupdated=[x for x in self.grasscoordinates2 if x not in set(self.rivercoordinates)]

        

    
    def create_river(self):
        blocks = []
        
        for (colonne, ligne) in self.rivercoordinates:
            block = BLOCK(colonne, ligne, 'river')
            blocks.append(block)
        
        return blocks
    
    def create_wall(self):
        blocks = []
        
        for (colonne, ligne) in self.wallcoordinates:
            block = BLOCK(colonne, ligne, 'wall')
            blocks.append(block)
        
        return blocks
    
    def create_grass(self):
        blocks=[]
        for (colonne, ligne) in self.grasscoordinatesupdated:
            block = BLOCK(colonne, ligne, 'grass')
            blocks.append(block)
        
        return blocks
        








    
    

        
    



