
import random
from block import *
from unit import Bombe

class Enemy:  

    def __init__(self,enemy, target, NOMove,enemy_list,unit_list,wall):
        self.enemy=enemy
        self.target=target
        self.NOMove= NOMove
        self.unit_list=unit_list
        self.enemy_list=enemy_list
        self.wall=wall

    def move_towards_target(self):
        
        possible_moves = []

        
        if (self.enemy.x + 1, self.enemy.y) not in self.NOMove and 0 <= self.enemy.x+1 < GRID_SIZE and 0 <= self.enemy.y < GRID_SIZE:
            possible_moves.append((1, 0))  # Move right

        
        if (self.enemy.x - 1, self.enemy.y) not in self.NOMove and 0 <= self.enemy.x+1 < GRID_SIZE and 0 <= self.enemy.y < GRID_SIZE:
            possible_moves.append((-1, 0))  # Move left

        
        if (self.enemy.x, self.enemy.y + 1) not in self.NOMove and 0 <= self.enemy.x+1 < GRID_SIZE and 0 <= self.enemy.y < GRID_SIZE:
            possible_moves.append((0, 1))  # Move down

        
        if (self.enemy.x, self.enemy.y - 1) not in self.NOMove and 0 <= self.enemy.x+1 < GRID_SIZE and 0 <= self.enemy.y < GRID_SIZE:
            possible_moves.append((0, -1))  # Move up

        
        if (self.enemy.x + 1, self.enemy.y - 1) not in self.NOMove and 0 <= self.enemy.x+1 < GRID_SIZE and 0 <= self.enemy.y < GRID_SIZE:
            possible_moves.append((1, -1))  # Move right and up

        
        if (self.enemy.x + 1, self.enemy.y + 1) not in self.NOMove and 0 <= self.enemy.x+1 < GRID_SIZE and 0 <= self.enemy.y < GRID_SIZE:
            possible_moves.append((1, 1))  # Move right and down

        
        if (self.enemy.x - 1, self.enemy.y - 1) not in self.NOMove and 0 <= self.enemy.x+1 < GRID_SIZE and 0 <= self.enemy.y < GRID_SIZE:
            possible_moves.append((-1, -1))  # Move left and up

        
        if (self.enemy.x - 1, self.enemy.y + 1) not in self.NOMove and 0 <= self.enemy.x+1 < GRID_SIZE and 0 <= self.enemy.y < GRID_SIZE:
            possible_moves.append((-1, 1))  # Move left and down

        
        if possible_moves:
            
            best_moves = []
            min_distance = float('inf')

            for dx, dy in possible_moves:
                new_x = self.enemy.x + dx
                new_y = self.enemy.y + dy
                distance_to_target = abs(new_x - self.target.x) + abs(new_y - self.target.y)

                
                if distance_to_target < min_distance:
                    best_moves = [(dx, dy)]
                    min_distance = distance_to_target
                elif distance_to_target == min_distance:
                    best_moves.append((dx, dy))

            dx, dy = random.choice(best_moves)
            return dx,dy
        else:
            dx,dy=0
            return dx,dy
    
    def attack_IA(self,chosen_attack,bombe_enemy,burnt_grass=[]):

                if chosen_attack == "Attack BOMB" and abs(self.enemy.x - self.target.x) <= self.enemy.distance_attack and abs(self.enemy.y - self.target.y) <= self.enemy.distance_attack:
                    # Decide target location for the bomb (Avoid Having 100% Precision each time)
                    bomb_target_x = random.choice([self.target.x + 1, self.target.x - 1, self.target.x])
                    bomb_target_y = random.choice([self.target.y + 1, self.target.y - 1, self.target.y])

                    # Place a bomb at the target location
                    new_bomb = Bombe(bomb_target_x, bomb_target_y,self.enemy.distance_attack,self.enemy.team)
                    new_bomb.move(bomb_target_x, bomb_target_y)
                    new_bomb.attack_bombe(self.unit_list,burnt_grass)
                    new_bomb.bombe_affected_zone(burnt_grass)
                    bombe_enemy.append(new_bomb)

                    if bombe_enemy:
                        bombe_enemy.remove(bombe_enemy[-1])
    
                if chosen_attack=="Attack 1":
                        if abs(self.enemy.x - self.target.x) <= self.enemy.distance_attack and abs(self.enemy.y - self.target.y) <= self.enemy.distance_attack:
                            self.enemy.attack1(WALL, self.unit_list)
 
                if chosen_attack=="Attack Trap":

                        trap_x = random.randint(self.enemy.x - self.enemy.distance_attack, self.enemy.x + self.enemy.distance_attack)
                        trap_y = random.randint(self.enemy.y - self.enemy.distance_attack, self.enemy.y + self.enemy.distance_attack)

                        new_bomb = Bombe(trap_x, trap_y,self.enemy.distance_attack,self.enemy.team)
                        new_bomb.move(trap_x, trap_y)
                        bombe_enemy.append(new_bomb)
                        new_bomb.attack_trap(self.unit_list, burnt_grass,bombe_enemy)
        

                if chosen_attack=="Teleportation":
                        directions=['Up','Down','Right','Left']
                        direction=random.choice(directions)
                        self.enemy.teleportation(direction)

                if chosen_attack=="Augmentation Defense" and abs(self.enemy.x - self.target.x) <= self.enemy.distance_attack and abs(self.enemy.y - self.target.y) <= self.enemy.distance_attack:
                        self.enemy.attack2()

                if chosen_attack=="Curing Power" and abs(self.enemy.x - self.target.x) <= self.enemy.distance_attack and abs(self.enemy.y - self.target.y) <= self.enemy.distance_attack:
                        self.enemy.attack3(self.enemy_list)

                if chosen_attack=="Augmentation Power" and abs(self.enemy.x - self.target.x) <= self.enemy.distance_attack and abs(self.enemy.y - self.target.y) <= self.enemy.distance_attack:
                        self.enemy.power_allies(self.enemy_list)

                if chosen_attack=="Attack Proche" and abs(self.enemy.x - self.target.x) <= 1 and abs(self.enemy.y - self.target.y) <= 1:
                     self.enemy.attack2(self.unit_list)

                if chosen_attack=="Attack Foudre" and abs(self.enemy.x - self.target.x) <= self.enemy.distance_attack and abs(self.enemy.y - self.target.y) <= self.enemy.distance_attack:
                     self.enemy.attack_foudre(self.unit_list)


                    
                        
     

                    
                                         


    