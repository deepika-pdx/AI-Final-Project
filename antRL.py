import random
import numpy as np
import pygame


class Ant:
    def __init__(self):
        self.no_of_ants = 5
        pygame.init()
        # Displaying a 800X600 game window
        self.window_x = 800
        self.window_y = 640
        self.window = pygame.display.set_mode((self.window_x, self.window_y))
        pygame.display.set_caption("Sugar hunt")
        # background image
        self.bg = pygame.image.load("greengrass.jpeg")
        self.window.blit(self.bg, (0, 0))
        self.ants = []
        self.ant_x = []
        self.ant_y = []
        self.wall = pygame.image.load("wall-1475318__480.jpeg")
        self.bread = pygame.image.load("bread.png")
        self.grid = []

    def load_ant(self):
        ant_xlist = list()
        ant_ylist = list()
        for x in range(self.window_x):
            if x % 80 == 0 and x < self.window_x/2:
                ant_xlist.append(x)
        for y in range(self.window_y):
            if y % 80 == 0 and y < self.window_y/2:
                ant_ylist.append(y)
        for i in range(self.no_of_ants):
            self.ants.append(pygame.image.load("ant_final.png"))
            self.ant_x.append(random.choice(ant_xlist))
            self.ant_y.append(random.choice(ant_ylist))

    def display_ant(self, x, y, i):
        self.load_ant()
        self.window.blit(self.ants[i], (x, y))

    def display_wall(self):
        self.window.blit(self.wall, (160, 160))

    def display_bread(self):
        self.window.blit(self.bread, (320, 0))

    def draw_grid(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        block_size = 80
        BLACK = (0, 0, 0)
        WHITE = (200, 200, 200)
        for x in range(SCREEN_WIDTH):
            for y in range(SCREEN_HEIGHT):
                rect = pygame.Rect(x*block_size, y*block_size,
                                   block_size, block_size)
                pygame.draw.rect(self.window, WHITE, rect, 1)

    def create_grid(self):
        self.grid = np.zeros((8, 10))
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if i == 2 and (j == 2 or j == 3 or j == 4 or j == 5 or j == 6 or j == 7):
                    self.grid[i][j] = -10
                elif i == 0 and j == 4:
                    self.grid[i][j] = 10
        return self.grid


ant = Ant()
print(ant.create_grid())
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for i in range(ant.no_of_ants):
        ant.display_ant(ant.ant_x[i], ant.ant_y[i], i). # ERROR after trying to generate ants inside cells
    ant.display_wall()
    ant.display_bread()
    ant.draw_grid(ant.window_x, ant.window_y)
    pygame.display.update()
pygame.quit()
