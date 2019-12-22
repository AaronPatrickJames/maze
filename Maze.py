import pygame
import random
import os
import sys

WIDTH = 600
HEIGHT = 800
BACKFILL = (50,50,50)
BALLS = 5
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)

gameDisplay = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Maze")
clock = pygame.time.Clock()

#Give the little dot its self
class dot:

    def __init__(self):
        self.x = 10
        self.y = 10
        self.score = 0 
        self.color = RED
        self.size = BALLS

    #resetdot, if dot hit wall
    def dead_dot(self):
        self.x = 10
        self.y = 10


#All the dots
class my_dot(dot):

    def lost_dot(self):
        pygame.draw.circle(gameDisplay,self.color,(self.x, self.y),self.size)
        
    def move_left(self):
        self.move_x = -2
        self.x += self.move_x
        if self.x < self.size: self.x = self.size

    def move_right(self):
        self.move_x = 2
        self.x += self.move_x
        if self.x >(WIDTH - self.size): self.x = (WIDTH - self.size)

    def move_up(self):
        self.move_y = -2
        self.y += self.move_y
        if self.y < self.size: self.y = self.size

    def move_down(self):
        self.move_y = 2
        self.y += self.move_y
        if self.y > (HEIGHT - self.size): self.y = (HEIGHT - self.size)


class key:

    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = BALLS * 2
        self.color = YELLOW

    #make new key, if key taken
    def new_key(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)


#Spawn a rng wall. (This might make the game unplayable) But if it was playable. That would be cool.
class wall_spawner:

    def __init__(self):
        self.size_w = random.randint(5, 200)
        self.size_h = random.randint(5, 200)
        self.color = WHITE
        self.x = random.randint(self.size_w + 10, (WIDTH - self.size_w))
        self.y = random.randint(self.size_h + 10, (WIDTH - self.size_h))


#put wall on screen
class spawn_wall(wall_spawner):

    def wallspawn(self):
        pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, self.size_w, self.size_h])
    

#spawn flag (win item)
class new_key_spawn(key):

    def spawn_key(self):
        pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, self.size, self.size])


#Check If Point is made
def check_add_score(lost, flag):
    if flag.x < (lost.x-lost.size) < (flag.x + flag.size) and flag.y < (lost.y-lost.size) < (flag.y + flag.size): #back of circle
        lost.score += 1
        flag.new_key()
    if flag.x < (lost.x-lost.size) < (flag.x + flag.size) and flag.y < (lost.y+lost.size) < (flag.y + flag.size): #top of circle
        lost.score += 1
        flag.new_key()
    if flag.x < (lost.x+lost.size) < (flag.x + flag.size) and flag.y < (lost.y-lost.size) < (flag.y + flag.size): #Bottom of circle
        lost.score += 1
        flag.new_key()
    if flag.x < (lost.x + lost.size) < (flag.x + flag.size) and flag.y < (lost.y+lost.size) < (flag.y + flag.size): #front of circle
        lost.score += 1
        flag.new_key()
    #this is a win case
    if lost.score == 10:
        #WinCaseHere!
        pass

#Checks to make sure a wall didnt spawn over the key
#if a wall has spawned over a key, it reset the wall placement
def check_wall_placement(barrier, flag):
    if barrier.x < flag.x < (barrier.x + barrier.size_w) and barrier.y < flag.y < (barrier.y + barrier.size_h): #top left corner of key in wall
        flag.new_key()
    if barrier.x < (flag.x + flag.size) < (barrier.x + barrier.size_w) and barrier.y < flag.y < (barrier.y + barrier.size_h):#top right corner of key in wall
        flag.new_key()
    if barrier.x < (flag.x + flag.size) < (barrier.x + barrier.size_w) and barrier.y < (flag.y+flag.size) < (barrier.y + barrier.size_h):#bottom right corner of key in wall
        flag.new_key()
    if barrier.x < flag.x < (barrier.x + barrier.size_w) and barrier.y < (flag.y+flag.size) < (barrier.y + barrier.size_h):#bottom left corner of key in wall
        flag.new_key()

def check_ball_placement(barrier, dot):
    if barrier.x < (dot.x - dot.size) < (barrier.x + barrier.size_w) and barrier.y < (dot.y-dot.size) < (barrier.y + barrier.size_h): #top left corner of key in wall
        dot.dead_dot()
    if barrier.x < (dot.x + dot.size) < (barrier.x + barrier.size_w) and barrier.y < (dot.y-dot.size) < (barrier.y + barrier.size_h):#top right corner of key in wall
        dot.dead_dot()
    if barrier.x < (dot.x + dot.size) < (barrier.x + barrier.size_w) and barrier.y < (dot.y+dot.size) < (barrier.y + barrier.size_h):#bottom right corner of key in wall
        dot.dead_dot()
    if barrier.x < (dot.x - dot.size) < (barrier.x + barrier.size_w) and barrier.y < (dot.y+dot.size) < (barrier.y + barrier.size_h):#bottom left corner of key in wall
        dot.dead_dot()
        
#if key pressed (that is valid key)
def keyboard_scanner(event, lost):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            lost.move_left()
        if event.key == pygame.K_RIGHT:
            lost.move_right()
        if event.key == pygame.K_UP:
            lost.move_up()
        if event.key == pygame.K_DOWN:
            lost.move_down()

#SpawnMultiWalls
def trumps_walls():
    walls = 10
    my_walls = dict(enumerate([spawn_wall() for i in range(walls)]))
    return my_walls

#wall list, prints walls and check to make sure none touch flag
def draw_walls(barrier, flag, lost):
    for barrier_id in barrier:
        my_wall = barrier[barrier_id]
        my_wall.wallspawn()
        check_wall_placement(my_wall, flag)
        check_ball_placement(my_wall, lost)#Check if dot is dead
        
        
#game logic loop
def gameLogic(lost, flag, barrier):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #check_wall_placement(barrier, flag)
                
        gameDisplay.fill(BACKFILL)#RemoveSpawnedItemScreenDrag
        flag.spawn_key()#SpawnKey
        lost.lost_dot()#SpawnFlag
        draw_walls(barrier, flag, lost)#SpawnWalls/CheckWalls
        keyboard_scanner(event, lost)#Check for keyboard event
        check_add_score(lost, flag)#Check for score counter update
        pygame.display.update()#display update to board
        clock.tick(60)#fps is 60, run 60 times a second (if possible) 
                
    
#main logloop
def main():
    lost = my_dot() #make user dot
    flag = new_key_spawn() #make flag
    barrier = trumps_walls() #make walls
    gameLogic(lost, flag, barrier)#rungame
                






if __name__ == "__main__":
    main()
