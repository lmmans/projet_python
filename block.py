import pygame
import random
from unit import *

BLOCKTYPES=['river','wall',"grass"]
BLOCKIMAGE={
    'river': pygame.image.load("water.png"),
    'wall': pygame.image.load("wall.png")
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
    
        self.rivercoordinates=[(2,0),(2,1),(3,0),(3,1),(3,2),(3,3),(4,2),(4,3),(4,4),(4,5)]
        self.wallcoordinates=[(0,5),(1,5),(6,5),(7,5),(6,0),(6,1),(6,2)]

    
    def create_river(self):
        blocks = []
        
        for (ligne, colonne) in self.rivercoordinates:
            block = BLOCK(colonne, ligne, 'river')
            blocks.append(block)
        
        return blocks
    
    def create_wall(self):
        blocks = []
        
        for (ligne, colonne) in self.wallcoordinates:
            block = BLOCK(colonne, ligne, 'wall')
            blocks.append(block)
        
        return blocks
    







    
    

        
    



