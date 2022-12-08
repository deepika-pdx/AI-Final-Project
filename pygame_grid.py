import random
import numpy as np
import pygame


class Ant:
    def __init__(self):
        self.no_of_ants = 5
        pygame.init()
        # Displaying a 800X600 game window
        self.ant_size = 30
        self.window_x = 800
        self.window_y = 640
        self.wall_x = 160
        self.wall_y = 160
        self.bread_x = 320
        self.bread_y = 0
        self.window = pygame.display.set_mode((self.window_x, self.window_y))
        pygame.display.set_caption("Sugar hunt")
        # background image
        self.bg = pygame.image.load("greengrass.jpg")
        self.window.blit(self.bg, (0, 0))
        self.ant = pygame.image.load("ant.png")
        self.ant_x = random.randrange(self.ant_size, self.window_x - self.ant_size)
        self.ant_y = random.randrange(self.window_y - self.ant_size, self.window_y) - self.ant_size
        self.wall = pygame.image.load("brick_wall.png")
        self.bread = pygame.image.load("icons8-bread-loaf-48.png")
        self.grid = []

    def display_ant(self):
        self.window.blit(self.ant, (self.ant_x, self.ant_y))

    def display_wall(self):
        self.window.blit(self.wall, (self.wall_x, self.wall_y))

    def display_bread(self):
        self.window.blit(self.bread, (self.bread_x, self.bread_y))

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

    # def load_background(self):
    #     # Reloading the background
    #     self.window.blit(self.bg, (0, 0))
    #     # Displaying the food
    #     food = pygame.image.load("icons8-bread-loaf-48.png")
    #     self.window.blit(food, (self.bread_x, self.bread_y))
    #     # Displaying the obstacle
    #     obstacle = pygame.image.load("brick_wall.png")
    #     obstacle_rect = obstacle.get_rect()
    #     obs_width = obstacle_rect.width
    #     obs_height = obstacle_rect.height
    #     self.window.blit(obstacle, (self.wall_x, self.wall_y))
    #     pygame.display.update()
    # #     #return obs_width, obs_height


ant = Ant()
print(ant.create_grid())
running = True
vel = 80
while running:
    #lspygame.time.delay(5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    # if left arrow key is pressed
    if keys[pygame.K_LEFT] and ant.ant_x > 0:
        # decrement in x co-ordinate
        ant.ant_x -= vel

    # if left arrow key is pressed
    if keys[pygame.K_RIGHT] and ant.ant_x <ant.window_x - ant.ant_size:
        # increment in x co-ordinate
        ant.ant_x += vel

    # if left arrow key is pressed
    if keys[pygame.K_UP] and ant.ant_y> 0:
        # decrement in y co-ordinate
        ant.ant_y -= vel

    # if left arrow key is pressed
    if keys[pygame.K_DOWN] and ant.ant_y < ant.window_y - ant.ant_size:
        # increment in y co-ordinate
        ant.ant_y += vel

    ant.display_ant()
    ant.display_wall()
    ant.display_bread()
    ant.draw_grid(ant.window_x, ant.window_y)
    pygame.display.update()

pygame.quit()

