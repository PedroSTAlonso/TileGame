import pygame, sys
from pygame.locals import *
from random import randint

class terrain():
    def __init__(self, terrain):
        self.terrain = terrain
        terrains = ["g", "w", "d", "s", "l"]
        colors = [(0, 255, 0), (0, 0, 255), (153, 76, 0), (0, 0, 255), (255, 255, 0)]
        self.color = colors[terrains.index(self.terrain)]

class enemy():
    def __init__(self, abrangence, direction, x, y):
        self.ab = abrangence
        self.hor = direction
        self.x = x
        self.y = y
        self.pos = [y, x]
        self.aX = x
        self.aY = y
        self.aPos = self.pos
        self.sum = 1

    def move(self):
        if not self.hor:
            if self.aX + self.sum > (self.x + self.ab) or self.aX + self.sum < self.x:
                self.sum = (-1)*self.sum
            self.aX = self.aX + self.sum
            
        else:
            if self.aY + self.sum > (self.y + self.ab) or self.aY + self.sum < self.y:
                self.sum = (-1)*self.sum
            self.aY = self.aY + self.sum

        self.aPos = [self.aY, self.aX]
            

backtile = [[]]
MAPWIDTH = 0
MAPHEIGHT = 0
enemies = []
enPos = []
char = [0, 0]
charType = [0, 0]
life = 3
game = [False, True, True]
tilemap = [[1]]
TILESIZE = 70
a = 0
winnis = -1

pygame.init()
win = pygame.display.set_mode((600, 600))
pygame.display.set_caption("TileTry")

print(game[2])
while True:

    pygame.time.delay(100)

    if game[0]:
        enPos = []
        for e in enemies:
            e.move()
            enPos.append(e.aPos)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and char[0] < MAPWIDTH:
            try:
                if tilemap[char[1]][char[0]+1] != "d":
                    char[0] += 1
            except IndexError:
                pass

        if keys[pygame.K_LEFT] and char[0] > 0:
            try:
                if tilemap[char[1]][char[0]-1] != "d":
                    char[0] -= 1
            except IndexError:
                pass

        if keys[pygame.K_UP] and char[1] > 0:
            try:
                if tilemap[char[1]-1][char[0]] != "d":
                    char[1] -= 1
            except IndexError:
                pass

        if keys[pygame.K_DOWN] and char[1] < MAPHEIGHT:
            try:
                if tilemap[char[1]+1][char[0]] != "d":
                    char[1] += 1
            except IndexError:
                pass

        for c in enemies:
            if (char[0] == c.aX) and (char[1] == c.aY):
                life -=1
                if life < 3:
                    charType[0] = 1
                    charType[1] = 0
        
        if life == 0:
            game = [False, False, False]
        
        for row in range(MAPHEIGHT):
            for column in range(MAPWIDTH):
                if ((char[0] == column and char[1] == row)) or ([row, column] in enPos):
                    if (char[0] == column and char[1] == row):
                        pygame.draw.rect(win, (0, 255, 0), (column*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))
                        if charType[0] == 2:
                            pygame.draw.ellipse(win, (randint(0, 255), randint(0, 255), randint(0, 255)), (column*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE)) ########
                        if charType[0] == 1:
                            if charType[1] <= 2:
                                pygame.draw.ellipse(win, (153, 76, 120), (column*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))
                                charType[1] += 1
                            elif charType[1] <= 4:
                                pygame.draw.ellipse(win, (255, 0, 0), (column*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))
                                charType[1] += 1
                            else:
                                charType[1] = 0
                        if charType[0] == 0:
                            pygame.draw.ellipse(win, (153, 76, 120), (column*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))
                    else:
                        pygame.draw.rect(win, (255, 0, 0), (column*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))
                    
                else:
                    pygame.draw.rect(win, terrain(tilemap[row][column]).color, (column*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))

        if char ==  [MAPHEIGHT-1, MAPWIDTH-1]:
            game = [False, True, False]

    else:
        if game[2]:
            charType = [0, 0]
            enemies = []
            life = 3
            char = [0, 0]
            if not game[0] and game[1]:
                tilemap[MAPWIDTH-1][MAPHEIGHT-1] = "g"
                winnis += 1
                MAPHEIGHT += 10
                MAPWIDTH += 10
                TILESIZE = int(600/MAPWIDTH)
                if int(TILESIZE) != 600:
                    win = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))
               
            for y in range(MAPHEIGHT):
                for x in range(MAPWIDTH):
                    backtile[y].append("g")
                backtile.append([])

                tilemap = backtile

            for i in range(randint((winnis+2)**2 + winnis, (winnis+3)**2 + 2*winnis)):
                k = randint(1, 2)
                if k == 1:
                    k = enemy(randint(2, MAPWIDTH-1), True, randint(1, MAPWIDTH-1), randint(1, MAPHEIGHT-1))
                else:
                    k = enemy(randint(2, MAPWIDTH-1), False, randint(1, MAPHEIGHT-1), randint(1, MAPHEIGHT-1))
                if not (k in enemies) and not((k.x == 0) and (k.y == 0)):
                    enemies.append(k)

            places = []
            
            for i in range(randint(6*(winnis+2), 6*(winnis+3))):
                k = [randint(0, MAPWIDTH-1), randint(0, MAPHEIGHT-1)]
                if not (k in places) and not (k[0] == 0 and k[1] == 0) and not(k[0] == MAPWIDTH-1 and k[1] == MAPHEIGHT-1):
                    places.append(k)
                    tilemap[k[0]][k[1]] = "d"

            tilemap[MAPWIDTH-1][MAPHEIGHT-1] = "l"
            a = 0
            game = [True, True, False]
        else:
            if game[1]:
                for i in range(a+1):
                    pygame.draw.rect(win, (255, 255, 0), ((i)*TILESIZE, (a-i)*TILESIZE, TILESIZE, TILESIZE))
                a += 1
            else:
                for i in range(a+1):
                    pygame.draw.rect(win, (255, 0, 0), (i*TILESIZE, (a-i)*TILESIZE, TILESIZE, TILESIZE))
                a += 1

            if a == (MAPHEIGHT + MAPWIDTH + 2):
                game = [False, game[1], True]
        
    pygame.display.update()
