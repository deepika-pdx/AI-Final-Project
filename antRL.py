import random
import numpy as np
import pygame


class Ant:
    def __init__(self):
        self.no_of_ants = 1
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
        self.ant_x = []
        self.ant_y = []
        for i in range(self.no_of_ants):
            self.ants.append(pygame.image.load("ant_final.png"))
            self.ant_x.append(random.randint(0, self.window_y/2))
            self.ant_y.append(random.randint(self.window_y/2, self.window_y-50))

        self.collection = 0
        self.reward = 0
 

    def display_ant(self, x, y, i):
        #self.load_ant()
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
        self.grid = np.zeros((10, 12))
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if (j == 0 or j == 11 or i == 0 or i == 9):
                    self.grid[i][j] = 3
                if i == 2 and (j == 2 or j == 3 or j == 4 or j == 5 or j == 6 or j == 7):
                    self.grid[i][j] = -10
                elif i == 1 and j == 4:
                    self.grid[i][j] = 10
        return self.grid

    def ant_curr_pos(self, i):
        x = self.ant_x[i]
        y = self.ant_y[i]


    def sense_curr(self, grid):
        return grid[self.x][self.y]

    def sense_north(self, grid):
        return grid[self.x][self.y + 1]

    def sense_south(self, grid):
        return grid[self.x][self.y - 1]

    def sense_east(self, grid):
        return grid[self.x + 1][self.y]

    def sense_west(self, grid):
        return grid[self.x - 1][self.y]

    def eat_food(self, grid):  # eat the bread
        if grid[self.x][self.y] == 10:
            grid[self.x][self.y] = 0
            return True  # if action was successful
        else:
            return False

    def wall(self, grid):
        if grid[self.x][self.y] == -10:  # if hit the wall
            return True 

    def move_north(self, grid):  # move north on the grid
        if self.sense_north(grid) == 3:
            return False
        self.y += 1
        return True  # if action was successful

    def move_south(self, grid):  # move south on the grid
        if self.sense_south(grid) == 3:
            return False
        self.y -= 1
        return True  # if action was successful

    def move_east(self, grid):  # move east on the grid
        if self.sense_east(grid) == 3:
            return False
        self.x += 1
        return True  # if action was successful

    def move_west(self, grid):  # move est on the grid
        if self.sense_west(grid) == 3:
            return False
        self.x -= 1
        return True  # if action was successful

    def convert_state(self, grid):  # represents state as a tuple
        state_vector = (self.sense_curr(grid), self.sense_north(grid), self.sense_south(grid), self.sense_east(grid), self.sense_west(grid))
        return state_vector

    def select_action(self, curr_state, Q_matrix, epsilon):
        if random.randint(1, 100) <= (100 * epsilon):
            action = random.randint(0, 4)
            return action
        poss_actions = list()  # list of possible action's q values
        eat = Q_matrix[curr_state][0]  # eat bread q value
        poss_actions.append(eat)
        N = Q_matrix[curr_state][1]  # move north q value
        poss_actions.append(N)
        S = Q_matrix[curr_state][2]  # move south q value
        poss_actions.append(S)
        E = Q_matrix[curr_state][3]  # move east q value
        poss_actions.append(E)
        W = Q_matrix[curr_state][4]  # move west q value
        poss_actions.append(W)
        Max = max(poss_actions)  # the max q value of all possible actions
        if Max == eat:
            action = 0
        if Max == N:
            action = 1
        elif Max == S:
            action = 2
        elif Max == E:
            action = 3
        else:
            action = 4
        return action

    def perform_action(self, action, grid):  # perform the action that was selected
        if action == 0:  # eat bread
            success = self.eat_food(grid)
            if success is True:
                self.collection += 1
                return 10
            else:
                return -1
        if action == 1:  # move North
            success = self.move_north(grid)
            if success is True:
                return 0
            else:
                return -5
        elif action == 2:  # move South
            success = self.move_south(grid)
            if success is True:
                return 0
            else:
                return -5
        elif action == 3:  # move East
            success = self.move_east(grid)
            if success is True:
                return 0
            else:
                return -5
        elif action == 4:  # move West
            success = self.move_west(grid)
            if success is True:
                return 0
            else:
                return -5

    def train(self, Q_matrix):
        N = 5000  # number of reps for training
        k = 0  # starting rep
        epsilon = 0.1  # greedy action selection
        reward_list = list()
        while k < N:
            grid = self.create_grid()  # creates grid
            for i, g in enumerate(grid):
                for j, gr in enumerate(grid[i]):
                    if j == 0 or j == 11 or i == 0 or i == 11:
                        grid[i][j] = 3
            self.x = random.randint(1, 10)
            self.y = random.randint(1, 10)
            self.Episode(grid, Q_matrix, epsilon)
            print(f'Total Reward: {self.reward}')
            print(f'Iteration: {k}')
            k += 1
            if ((N - k) % 50 == 0):  # every 50 reps reduce the epsilon value by .001
                epsilon -= 0.001
                reward_list.append(self.reward)

ant = Ant()
print(ant.create_grid())
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for i in range(ant.no_of_ants):
        ant.display_ant(ant.ant_x[i], ant.ant_y[i], i)  # ERROR after trying to generate ants inside cells
    ant.display_wall()
    ant.display_bread()
    ant.draw_grid(ant.window_x, ant.window_y)
    pygame.display.update()
pygame.quit()

