import random
import numpy as np
import pygame


def create_grid():
    grid = np.zeros((10, 12))
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if j == 0 or j == 11 or i == 0 or i == 9:
                grid[i][j] = 3
            if i == 2 and (j == 2 or j == 3 or j == 4 or j == 5 or j == 6 or j == 7):
                grid[i][j] = -10
            elif i == 1 and j == 4:
                grid[i][j] = 10
    return grid


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
        # self.ants = []
        # self.ant_x = []
        # self.ant_y = []
        self.wall = pygame.image.load("wall-1475318__480.jpeg")
        self.bread = pygame.image.load("bread.png")
        self.grid = []
        ''' for i in range(self.no_of_ants):
                self.ants.append(pygame.image.load("ant_final.png"))
                self.ant_x.append(random.randint(0, self.window_y/2))
                self.ant_y.append(random.randint(self.window_y/2, self.window_y-50))'''
        self.ant_size = 30
        self.box_size = 80
        self.ants = pygame.image.load("ant_final.png")
        self.ant_x = random.randrange(self.ant_size + self.box_size, self.window_x - self.ant_size)
        self.ant_y = random.randrange(self.window_y - (self.ant_size + self.box_size), self.window_y) - self.ant_size
        self.collection = 0
        self.reward = 0

    def display_ant(self, x, y):
        #self.load_ant()
        self.window.blit(self.ants, (x, y))

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
        if random.randint(1, 100) <= (100 * epsilon):  # exploring
            action = random.randint(0, 5)
            return action
        # exploiting
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
        wall = Q_matrix[curr_state][5]  # hit the obstacle(wall)
        poss_actions.append(wall)
        Max = max(poss_actions)  # the max q value of all possible actions
        if Max == eat:
            action = 0
        if Max == N:
            action = 1
        elif Max == S:
            action = 2
        elif Max == E:
            action = 3
        elif Max == 4:
            action = 4
        else:
            action = 5
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

    def episode(self, grid, Q_matrix, epsilon):
        M = 200  # number of reps
        n = 0.2  # learning rate
        y = 0.9
        i = 0  # starting rep
        while (i < M):
            curr_state = self.convert_state(grid)
            if curr_state not in Q_matrix:  # if first time seeing state then add to Q_matrrix
                Q_matrix[curr_state] = np.zeros(5)
            action = self.select_action(curr_state, Q_matrix, epsilon)
            reward = self.perform_action(action, grid)
            self.reward += reward
            new_state = self.convert_state(grid)
            if new_state not in Q_matrix:  # if first time seeing state then add to Q_matrrix
                Q_matrix[new_state] = np.zeros(5)
            Q_matrix[curr_state][action] = Q_matrix[curr_state][action] + n * (
                        reward + y * max(Q_matrix[new_state]) - Q_matrix[curr_state][action])
            i += 1


    def train(self, Q_matrix, grid):
        N = 5000  # number of reps for training
        k = 0  # starting rep
        epsilon = 0.1  # greedy action selection
        reward_list = list()
        while k < N:
            # grid = self.create_grid()  # creates grid
            for i, g in enumerate(grid):
                for j, gr in enumerate(grid[i]):
                    if j == 0 or j == 11 or i == 0 or i == 11:
                        grid[i][j] = 3
            self.x = random.randint(1, 10)
            self.y = random.randint(1, 10)
            #            print ("Before:")
            #            print (grid)
            self.episode(grid, Q_matrix, epsilon)
            #            print ("After:")
            #            print (grid)
            #  print("Cans Collected:")
            #  print(self.collection)
            print(f'Total Reward: {self.reward}')
            #  print("Points lost:")
            #  lost = ((self.collection * 10) - self.reward)
            #  print(lost)
            print(f'Iteration: {k}')
            k += 1
            if ((N - k) % 50 == 0):  # every 50 reps reduce the epsilon value by .001
                epsilon -= 0.001
                reward_list.append(self.reward)

    def test_episode(self, grid, Q_matrix, epsilon):
        M = 200  # number of reps
        i = 0  # starting rep
        while (i < M):
            curr_state = self.convert_state(grid)
            action = self.select_action(curr_state, Q_matrix, epsilon)
            reward = self.perform_action(action, grid)
            self.reward += reward
            i += 1

    def test(self, Q_matrix):
        N = 5000  # number of reps for testing
        k = 0  # starting rep
        epsilon = 0.1  # greedy action selection
        reward_list = list()
        while (k < N):
            self.grid = np.random.randint(2, size=(12, 12))  # creates grid
            for i, g in enumerate(self.grid):
                for j, gr in enumerate(self.grid[i]):
                    if j == 0 or j == 11 or i == 0 or i == 11:
                        self.grid[i][j] = 3
            self.x = random.randint(1, 10)
            self.y = random.randint(1, 10)
            self.collection = 0
            self.reward = 0
            self.test_episode(self.grid, Q_matrix, epsilon)
            reward_list.append(self.reward)
            k += 1
        z = 0


print(create_grid())
Q_matrix = {}
ant = Ant()
ant.train(Q_matrix, create_grid())  # trains ant
ant.test(Q_matrix)  # tests ant
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for i in range(ant.no_of_ants):
        ant.display_ant(ant.ant_x, ant.ant_y)  # ERROR after trying to generate ants inside cells
    ant.display_wall()
    ant.display_bread()
    ant.draw_grid(ant.window_x, ant.window_y)
    pygame.display.update()
pygame.quit()
