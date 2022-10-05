from random import randint
import pygame, sys

MAP_HEIGHT = 15
MAP_WIDTH = 15
MINES_COUNT = 30
MINE_VALUE = 9
BLACK = 0, 0, 0
GREY = 128, 128, 128
LGREY = 192, 192, 192
RED = (255, 0, 0)
TSIZE = 20

class Minesweeper:
    def __init__(self, height, width, count):
        self.map = []
        self.height = height
        self.width = width
        self.count = count
        self.game_on = True
        self.flag_count = 0
        for _ in range(self.height):
            l = []
            for _ in range(self.width):
                l.append({"v":0, "shown":0, "flag":0})
            self.map.append(l)

        for _ in range(self.count):
            x = randint(0, self.width - 1)
            y = randint(0, self.height - 1)
            while self.map[y][x]["v"] == MINE_VALUE: #-1 => mina 
                x = randint(0, self.width - 1)
                y = randint(0, self.height - 1)
            self.map[y][x]["v"] = MINE_VALUE
            for yy in range(-1, 2, 1):
                for xx in range(-1, 2, 1):
                    if xx != 0 or yy != 0: # ta mina
                        dy = y + yy
                        dx = x + xx
                        if (dx >= 0) and (dx < self.width) and (dy >= 0) and (dy < self.height): # miesci sie na planszy
                            if self.map[dy][dx]["v"] != MINE_VALUE: # nie ma tu miny
                                self.map[dy][dx]["v"] += 1
    def flag(self, y, x):
        if self.map[y][x]["shown"] == 0:
            if self.map[y][x]["flag"] == 0:
                self.map[y][x]["flag"] = 1
                self.flag_count += 1
            else:
                self.map[y][x]["flag"] = 0
                self.flag_count -= 1
            #self.map[y][x]["flag"] = 1 - self.map[y][x]["flag"]
            #self.flag_count = self.flag_count + (self.map[y][x]["flag"] * 2) - 1


    def reveal(self, y, x):
        if self.map[y][x]["shown"] == 0:
            self.map[y][x]["shown"] = 1
            if self.map[y][x]["flag"] == 1:
                self.map[y][x]["flag"] = 0
                self.flag_count -= 1
            if self.map[y][x]["v"] == 9:
                for dy in range(self.height):
                    for dx in range(self.width):
                        self.map[dy][dx]["shown"] = 1
                self.game_on = False
            elif self.map[y][x]["v"] == 0:
                for yy in range(-1, 2, 1):
                    for xx in range(-1, 2, 1):
                        if yy != 0 or xx != 0:
                            dy = y + yy
                            dx = x + xx 
                            if (dy >= 0) and (dy < self.height) and (dx >= 0) and (dx < self.width):
                                self.reveal(dy, dx)

    def show_map(self):
        for y in self.map:
            for x in y:
                if (x["shown"] == 1):  #1 to pole jest odkryte
                    print(x["v"], end=" ")
                else:
                    print("#", end = " ")
            print()
        print()

    def draw_map(self, screen):
        screen.fill(BLACK)
        c_shown = 0
        for y in range(self.height):
            top = TSIZE * y
            for x in range(self.width):
                left = TSIZE * x
                if self.map[y][x]["shown"] == 0:
                    pygame.draw.rect(screen, BLACK, (left, top, TSIZE, TSIZE))
                    pygame.draw.rect(screen, GREY, (left + 1, top + 1, TSIZE - 2, TSIZE - 2))
                    if self.map[y][x]["flag"] == 1:
                        dx = TSIZE - 6
                        dy = int(dx / 2)
                        pygame.draw.rect(screen, (0, 87, 183), (left + 3, top + 3, dx, dy))
                        pygame.draw.rect(screen, (255, 215, 0), (left + 3, top + 3 + dy, dx, dy))
                else:
                    c_shown += 1
                    if self.map[y][x]["v"] == 0:
                        pygame.draw.rect(screen, GREY, (left, top, TSIZE, TSIZE))
                        pygame.draw.rect(screen, LGREY, (left + 1, top + 1, TSIZE - 2, TSIZE - 2))
                    elif self.map[y][x]["v"] < 9:
                        font = pygame.font.SysFont(None, int(TSIZE * 1.2))
                        text = font.render(str(self.map[y][x]["v"]), True, LGREY)
                        screen.blit(text, [left + (TSIZE / 2) - (text.get_size()[0] / 2), top + (TSIZE / 2) - (text.get_size()[1] / 2)])
                    else:
                        pygame.draw.circle(screen, (255, 0, 0), (left + (TSIZE / 2), top + (TSIZE / 2)), TSIZE / 4)
        pygame.draw.circle(screen, (255, 0, 0), (TSIZE/2, (TSIZE * self.height) + (TSIZE / 2)), TSIZE / 4)
        font = pygame.font.SysFont(None, int(TSIZE * 1.2))
        text = font.render(str(self.count - self.flag_count), True, LGREY)
        screen.blit(text, (TSIZE, (TSIZE * self.height) + (TSIZE / 2) - (text.get_size()[1] / 2)))
        if self.flag_count == self.count and (self.height * self.width) - self.count == c_shown:
            self.game_on = False
            patron = pygame.image.load("ms.png")
            screen.blit(patron, ((TSIZE * self.width - patron.get_width()) / 2, (TSIZE * self.height - patron.get_height()) / 2, patron.get_width(), patron.get_height()))
            font = pygame.font.SysFont(None, int(TSIZE * 3))
            text = font.render(str("F*CK PTN"), True, RED)
            screen.blit(text, ((TSIZE * self.width - text.get_width()) / 2, ((TSIZE * self.height + patron.get_height()) / 2) + 10, text.get_width(), text.get_height()))

        pygame.display.flip()
                    
size = width, height = TSIZE * MAP_WIDTH, TSIZE * (MAP_HEIGHT + 1)
pygame.init()
pygame.display.set_caption("Сапер Патрон")
screen = pygame.display.set_mode(size)
a = Minesweeper(MAP_HEIGHT, MAP_WIDTH, MINES_COUNT)
# a.show_map()
a.draw_map(screen)
while True:
    #cy = int(input("Wiersz: "))
    #cx = int(input("Kolumna: "))
    #a.reveal(cy, cx)
    #a.show_map()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if a.game_on:
                x = int(event.pos[0] / TSIZE)
                y = int(event.pos[1] / TSIZE)
                if event.button == 1:
                    #print(event)
                    a.reveal(y, x)
                    a.draw_map(screen)
                elif event.button == 3:
                    a.flag(y, x)
                    a.draw_map(screen)
            else:
                pygame.quit()
                sys.exit()
    
