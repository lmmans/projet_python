import pygame
import random
from unit import *

BLOCKTYPES=['river','empty']
BLOCKIMAGE={
    'river': pygame.image.load("water.png"),
    'empty': pygame.image.load("empty.png")
}

class BLOCK:
    def __init__(self, x, y, block_type):
        self.x = x
        self.y = y
        self.block_type = block_type
        self.image = BLOCKIMAGE[block_type]

    def draw(self, screen):
        if self.block_type == 'river':
            scaled_image = pygame.transform.scale(self.image, (CELL_SIZE,CELL_SIZE))
            screen.blit(scaled_image, (self.x * CELL_SIZE, self.y * CELL_SIZE))

class GenerateBlocks:
    def __init__(self, lignes, colonnes,block_type):
        self.lignes = lignes
        self.colonnes = colonnes
        self.image = BLOCKIMAGE[block_type]
    
    def generateriver(self):
        riverpath = []
        riverstart = random.randint(0, self.colonnes - 1)
        colonne = riverstart
        ligne = 0

        direction = ['left', 'right', 'straight']
        lastdirectiontaken=''
        directionstaken=[]
        riverpath.append((ligne, colonne))


        while ligne < self.lignes and colonne < self.colonnes:
            directionprise = random.choice(direction)

            while lastdirectiontaken==directionprise:
                directionprise = random.choice(direction)
            
            directionstaken.append(lastdirectiontaken)

            if len(directionstaken)>3:

                if directionprise == 'left' and colonne > 0 and directionstaken[-3]!='left':
                    colonne -= 1
                elif directionprise == 'right' and colonne < self.colonnes - 1 and directionstaken[-3]!='right':
                    colonne += 1
                elif directionprise == 'straight':
                    ligne += 1

            else:

                if directionprise == 'left' and colonne > 0:
                    colonne -= 1
                elif directionprise == 'right' and colonne < self.colonnes - 1:
                    colonne += 1
                elif directionprise == 'straight':
                    ligne += 1

            riverpath.append((ligne, colonne))

            lastdirectiontaken = directionprise

            if ligne >= self.lignes or colonne >= self.colonnes:
                break

        return riverpath
    
    def create_river(self):
        riverpath = self.generateriver()
        blocks = []
        
        for (ligne, colonne) in riverpath:
            block = BLOCK(colonne, ligne, 'river')
            blocks.append(block)
        
        return blocks
    
    def bridge(self,riverpath,clear=45):

        numberofbridges = int(len(riverpath) * (clear / 100))
        bridges= riverpath[:]
        for _ in range(numberofbridges):
            if bridges:
                clear_water = random.choice(bridges)
                bridges.remove(clear_water)

        return bridges
    
    

        
    



