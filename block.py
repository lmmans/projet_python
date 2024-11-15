import pygame
import random
from unit import *

BLOCKTYPES=['river','wall']
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
    
    def _generateriver(self):
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
        riverpath = self._generateriver()
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
    

    
    def _generatewall(self,blocks,numberofwallswanted):
        wallcoordinates=[]
        visited=set(blocks)
        
        for i in range(numberofwallswanted-1):

            
            numberofblocks=random.randint(2,4)
            wallstart_ligne= random.randint(0, self.lignes - 1)
            wallstart_colonne = random.randint(0, self.colonnes - 1)


            # Securite 1ere et derniere colonnes et 1ere et derniere lgne 
            if wallstart_colonne == 0 and (wallstart_ligne != 0 and wallstart_ligne != self.lignes - 1):  #Condition Colonne 0
                directiontaken = random.choice(['right', 'straight'])
            elif wallstart_colonne == self.colonnes - 1 and (wallstart_ligne != 0 and wallstart_ligne != self.lignes - 1):  # Derniere Colonne
                directiontaken = random.choice(['left', 'straight'])
            elif (wallstart_ligne == 0 and wallstart_colonne != 0 and wallstart_colonne != self.colonnes - 1):  #premiereligne
                directiontaken = random.choice(['left', 'right'])
            elif (wallstart_ligne == self.lignes - 1 and wallstart_colonne!= 0 and wallstart_colonne!= self.colonnes - 1):  #dernierecolonne
                directiontaken = random.choice(['left', 'right'])

            #Securite Coins 
            elif wallstart_ligne == 0 and wallstart_colonne == 0:  
                directiontaken = 'right'
            elif wallstart_ligne == 0 and wallstart_colonne == self.colonnes - 1:  
                directiontaken = 'left'
            elif wallstart_ligne== self.lignes - 1 and wallstart_colonne == 0: 
                directiontaken = 'right'
            elif wallstart_ligne == self.lignes - 1 and wallstart_colonne == self.colonnes - 1: 
                directiontaken = 'left'

            #Condion générale 
            else:  
                directiontaken = random.choice(['left', 'right','straight'])


                   
            for block_index in range(numberofblocks):

                if directiontaken == 'left':
                    new_col = wallstart_colonne - block_index
                    if new_col < 0 or (new_col, wallstart_ligne) in visited:
                        break
                    wallcoordinates.append((new_col, wallstart_ligne))
                    visited.add((new_col, wallstart_ligne))

                elif directiontaken == 'right':
                    new_col = wallstart_colonne + block_index
                    if new_col >= self.colonnes or (new_col, wallstart_ligne) in visited:
                        break
                    wallcoordinates.append((new_col, wallstart_ligne))
                    visited.add((new_col, wallstart_ligne))

                elif directiontaken == 'straight':
                    new_row = wallstart_ligne + block_index
                    if new_row >= self.lignes or (wallstart_colonne, new_row) in visited:
                        break
                    wallcoordinates.append((wallstart_colonne, new_row))
                    visited.add((wallstart_colonne, new_row))

        return wallcoordinates
    
    def create_wall(self,blocks):
        numberofwalls=random.randint(1,3)
        wallpath= self._generatewall(blocks,numberofwalls)
        blocks = []
        
        for (colonne, ligne) in wallpath:
            block = BLOCK(colonne, ligne, 'wall')
            blocks.append(block)
        print(f"Generated walls: {len(blocks)}")
        
        return blocks
    
    def create_wall2(self, blocks):
        number_of_walls = random.randint(1, 3)
        retries = 30  # Maximum retry attempts
        wallpath = []

        for _ in range(retries):
            wallpath = self._generatewall(blocks, number_of_walls)
            if wallpath:  # If wallpath is not empty, break the loop
                break
            print("Retrying wall generation...")

        if not wallpath:
            print("Failed to generate walls after retries.")
        else:
            print(f"Generated {len(wallpath)} walls.")

        wall_blocks = [BLOCK(col, row, 'wall') for (col, row) in wallpath]
        return wall_blocks






    
    

        
    



