import random
import numpy as np
import pygame
from numpy import mean
from numpy.random import choice
import matplotlib.pyplot as plt
import statistics as st

clock = pygame.time.Clock()


class Ant:
    def __init__(self):
        pygame.init()
        # Displaying a 800X600 game window
        self.ant_size = 30
        self.window_x = 800
        self.window_y = 800
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
        self.bread = pygame.image.load("bread.png")
        self.grid = []

        self.Q_matrix = []
        self.actions = ["Move_North", "Move_South", "Move_East", "Move_West", "Eat_Food"]
        self.epsilon = 0.9
        self.eta = 0.2
        self.gamma = 0.9
        self.no_of_episodes = 20
        self.no_of_steps_in_each_episode = 100
        self.rewards_per_episode = []
        self.training_episode_value = []
        self.training_reward_value = []

    def display_ant(self):
        self.window.blit(self.ant, (self.ant_x * 80, self.ant_y * 80))

    def display_wall(self):
        self.window.blit(self.bg, (0, 0))
        self.window.blit(self.wall, (self.wall_x, self.wall_y))

    def display_bread(self):
        self.window.blit(self.bread, (self.bread_x, self.bread_y))

    def draw_grid(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        block_size = 80
        WHITE = (200, 200, 200)
        for x in range(SCREEN_WIDTH):
            for y in range(SCREEN_HEIGHT):
                rect = pygame.Rect(x * block_size, y * block_size,
                                   block_size, block_size)
                pygame.draw.rect(self.window, WHITE, rect, 1)

    def create_grid(self):
        self.grid = np.zeros((10, 10))
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if i == 2 and (j == 2 or j == 3 or j == 4 or j == 5 or j == 6 or j == 7):
                    self.grid[i][j] = -10
                elif (i == 0 and (j == 4 or j == 3 or j == 5)) or (i == 1 and j == 4):
                    self.grid[i][j] = 10
        return self.grid

    def generate_Q_matrix(self):
        first_row = ["Q(s,a)", "Move_North", "Move_South", "Move_East", "Move_West", "Eat_Food"]
        self.Q_matrix.append(first_row)
        for i in range(10):
            for j in range(10):
                each_row = [(i, j)]
                each_row.append([0 for k in range(5)])
                self.Q_matrix.append(each_row)

    def get_sensor_info(self, ant_x_pos, ant_y_pos):
        sensor_info = []
        # Determine current position state using sensor
        if self.grid[ant_x_pos][ant_y_pos] == 10:
            sensor_info.append("Food")
        elif self.grid[ant_x_pos][ant_y_pos] == -10:
            sensor_info.append("Obstacle")
        else:
            sensor_info.append("Empty")

        # Determine north state wrt current position using sensor
        if ant_x_pos - 1 < 0:
            sensor_info.append("Wall")
        elif self.grid[ant_x_pos - 1][ant_y_pos] == 10:
            sensor_info.append("Food")
        elif self.grid[ant_x_pos - 1][ant_y_pos] == -10:
            sensor_info.append("Obstacle")
        else:
            sensor_info.append("Empty")

        # Determine south state wrt current position using sensor
        if ant_x_pos + 1 > 9:
            sensor_info.append("Wall")
        elif self.grid[ant_x_pos + 1][ant_y_pos] == 10:
            sensor_info.append("Food")
        elif self.grid[ant_x_pos + 1][ant_y_pos] == -10:
            sensor_info.append("Obstacle")
        else:
            sensor_info.append("Empty")

        # Determine east state wrt current position using sensor
        if ant_y_pos + 1 > 9:
            sensor_info.append("Wall")
        elif self.grid[ant_x_pos][ant_y_pos + 1] == 10:
            sensor_info.append("Food")
        elif self.grid[ant_x_pos][ant_y_pos + 1] == -10:
            sensor_info.append("Obstacle")
        else:
            sensor_info.append("Empty")

        # Determine west state wrt current position using sensor
        if ant_y_pos - 1 < 0:
            sensor_info.append("Wall")
        elif self.grid[ant_x_pos][ant_y_pos - 1] == 10:
            sensor_info.append("Food")
        elif self.grid[ant_x_pos][ant_y_pos - 1] == -10:
            sensor_info.append("Obstacle")
        else:
            sensor_info.append("Empty")

        return sensor_info

    def select_an_action(self, x_pos, y_pos):

        if np.random.random() < self.epsilon:
            selected_action_index = np.argmax(self.Q_matrix[((x_pos * 10) + y_pos + 1)][1])
        else:
            selected_action_index = np.random.randint(0, 5)

        action = self.actions[selected_action_index]
        return action


ant = Ant()
ant.generate_Q_matrix()
running = True
vel = 80
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # ---------------------------------------------------------Training----------------------------------------------------------------------
    # for each episode
    for episode in range(ant.no_of_episodes):
        print("Episode number: " + str(episode))

        ant.grid = []
        ant.create_grid()
        print("Print initial grid: " + str(ant.grid))

        ant_current_x = random.randint(0, 9)
        ant_current_y = random.randint(0, 9)
        rewards_in_this_episode = 0
        no_of_times_reached_food = 0
        no_of_times_clashed_obstacle = 0

        ant.ant_x = ant_current_x
        ant.ant_y = ant_current_y

        # Reducing the value of epsilon after every 5 episodes
        if (ant.epsilon != 0 and episode != 0 and episode % 5 == 0):
            ant.epsilon -= 0.01

        for time_step in range(ant.no_of_steps_in_each_episode):
            ant.display_wall()
            ant.display_bread()
            ant.draw_grid(ant.window_x, ant.window_y)
            ant.display_ant()
            pygame.display.update()
            clock.tick(20)

            reward = 0
            # Choose an action using epsilon-greedy action selection
            selected_action = ant.select_an_action(ant_current_x, ant_current_y)
            ant_sensor_info = ant.get_sensor_info(ant_current_x, ant_current_y)

            ant_next_x = 0
            ant_next_y = 0
            if selected_action == "Eat_Food":
                if ant_sensor_info[0] == "Food":
                    reward = 100
                    no_of_times_reached_food += 1
                    ant_next_x = ant_current_x
                    ant_next_y = ant_current_y
                elif ant_sensor_info[0] == "Obstacle":
                    reward = -50
                    no_of_times_clashed_obstacle += 1
                    ant_next_x = random.randint(0, 9)
                    ant_next_y = random.randint(0, 9)
                else:
                    reward = -10
                    ant_next_x = ant_current_x
                    ant_next_y = ant_current_y
            elif selected_action == "Move_North":
                if ant_sensor_info[1] == "Wall":
                    reward = -10
                    ant_next_x = ant_current_x
                    ant_next_y = ant_current_y
                elif ant_sensor_info[1] == "Obstacle":
                    reward = -50
                    ant_next_x = random.randint(0, 9)
                    ant_next_y = random.randint(0, 9)
                else:
                    ant_next_x = ant_current_x - 1
                    ant_next_y = ant_current_y
            elif selected_action == "Move_South":
                if ant_sensor_info[2] == "Wall":
                    reward = -10
                    ant_next_x = ant_current_x
                    ant_next_y = ant_current_y
                elif ant_sensor_info[2] == "Obstacle":
                    reward = -50
                    ant_next_x = random.randint(0, 9)
                    ant_next_y = random.randint(0, 9)
                else:
                    ant_next_x = ant_current_x + 1
                    ant_next_y = ant_current_y
            elif selected_action == "Move_East":
                if ant_sensor_info[3] == "Wall":
                    reward = -10
                    ant_next_x = ant_current_x
                    ant_next_y = ant_current_y
                elif ant_sensor_info[3] == "Obstacle":
                    reward = -50
                    ant_next_x = random.randint(0, 9)
                    ant_next_y = random.randint(0, 9)
                else:
                    ant_next_x = ant_current_x
                    ant_next_y = ant_current_y + 1
            else:
                if ant_sensor_info[4] == "Wall":
                    reward = -10
                    ant_next_x = ant_current_x
                    ant_next_y = ant_current_y
                elif ant_sensor_info[4] == "Obstacle":
                    reward = -50
                    ant_next_x = random.randint(0, 9)
                    ant_next_y = random.randint(0, 9)
                else:
                    ant_next_x = ant_current_x
                    ant_next_y = ant_current_y - 1

            # Getting current state Q(s,a) value from Q-matrix
            q_matrix_current_x = (ant_current_x * 10) + ant_current_y + 1
            q_matrix_current_y = ant.actions.index(selected_action)
            Qsa_row = ant.Q_matrix[q_matrix_current_x][1]
            Qsa_current_value = Qsa_row[q_matrix_current_y]

            # Getting next state max(Q(s,a)) value from Q-matrix
            q_matrix_next_x = (ant_next_x * 10 + ant_next_y) + 1
            Qsa_next_row = ant.Q_matrix[q_matrix_next_x][1]
            Qsa_next_max_value = max(Qsa_next_row)

            # Calculating the updated values of Q(s,a) using Q-Learning algorithm
            Qsa_updated_value = Qsa_current_value + ant.eta * (
                    reward + (ant.gamma * Qsa_next_max_value) - Qsa_current_value)

            # Updating the new Q(s,a) value in original Q-matrix
            ant.Q_matrix[q_matrix_current_x][1][q_matrix_current_y] = Qsa_updated_value

            rewards_in_this_episode += reward

            ant_current_x = ant_next_x
            ant_current_y = ant_next_y

            ant.ant_x = ant_current_x
            ant.ant_y = ant_current_y

        print("Rewards in this episode: " + str(rewards_in_this_episode))
        print("Count of times ant reached food in this episode: " + str(no_of_times_reached_food))
        print("Count of times ant clashed obstacle in this episode: " + str(no_of_times_clashed_obstacle))
        ant.rewards_per_episode.append(rewards_in_this_episode)
        ant.training_episode_value.append(episode)
        ant.training_reward_value.append(rewards_in_this_episode)

    plt.title("Training reward plot (rewards vs episode number)")
    plt.xlabel("Episode number")
    plt.ylabel("Total rewards in the episode")
    plt.plot(ant.training_episode_value, ant.training_reward_value)
    plt.show()

    # ---------------------------------------------------------Testing----------------------------------------------------------------------

    ant.rewards_per_episode = []
    ant.training_episode_value = []
    ant.training_reward_value = []
    # for each episode
    for episode in range(ant.no_of_episodes):
        print("Episode number: " + str(episode))

        ant.grid = []
        ant.create_grid()
        print("Print initial grid: " + str(ant.grid))

        ant_current_x = random.randint(0, 9)
        ant_current_y = random.randint(0, 9)
        rewards_in_this_episode = 0
        no_of_times_reached_food = 0
        no_of_times_clashed_obstacle = 0

        ant.ant_x = ant_current_x
        ant.ant_y = ant_current_y

        # # Reducing the value of epsilon after every 50 episodes
        ant.epsilon = 0.9

        for time_step in range(ant.no_of_steps_in_each_episode):
            ant.display_wall()
            ant.display_bread()
            ant.draw_grid(ant.window_x, ant.window_y)
            ant.display_ant()
            pygame.display.update()

            reward = 0
            # Choose an action using epsilon-greedy action selection
            selected_action = ant.select_an_action(ant_current_x, ant_current_y)
            ant_sensor_info = ant.get_sensor_info(ant_current_x, ant_current_y)

            ant_next_x = 0
            ant_next_y = 0
            if selected_action == "Eat_Food":
                if ant_sensor_info[0] == "Food":
                    reward = 100
                    no_of_times_reached_food += 1
                    ant_next_x = ant_current_x
                    ant_next_y = ant_current_y
                elif ant_sensor_info[0] == "Obstacle":
                    reward = -20
                    no_of_times_clashed_obstacle += 1
                    ant_next_x = random.randint(0, 9)
                    ant_next_y = random.randint(0, 9)
                else:
                    reward = -5
                    ant_next_x = ant_current_x
                    ant_next_y = ant_current_y
            elif selected_action == "Move_North":
                if ant_sensor_info[1] == "Wall":
                    reward = -5
                    ant_next_x = ant_current_x
                    ant_next_y = ant_current_y
                elif ant_sensor_info[1] == "Obstacle":
                    reward = -20
                    ant_next_x = random.randint(0, 9)
                    ant_next_y = random.randint(0, 9)
                else:
                    reward = 5
                    ant_next_x = ant_current_x - 1
                    ant_next_y = ant_current_y
            elif selected_action == "Move_South":
                if ant_sensor_info[2] == "Wall":
                    reward = -5
                    ant_next_x = ant_current_x
                    ant_next_y = ant_current_y
                elif ant_sensor_info[2] == "Obstacle":
                    reward = -20
                    ant_next_x = random.randint(0, 9)
                    ant_next_y = random.randint(0, 9)
                else:
                    reward = -2
                    ant_next_x = ant_current_x + 1
                    ant_next_y = ant_current_y
            elif selected_action == "Move_East":
                if ant_sensor_info[3] == "Wall":
                    reward = -5
                    ant_next_x = ant_current_x
                    ant_next_y = ant_current_y
                elif ant_sensor_info[3] == "Obstacle":
                    reward = -20
                    ant_next_x = random.randint(0, 9)
                    ant_next_y = random.randint(0, 9)
                else:
                    reward = 2
                    ant_next_x = ant_current_x
                    ant_next_y = ant_current_y + 1
            else:
                if ant_sensor_info[4] == "Wall":
                    reward = -5
                    ant_next_x = ant_current_x
                    ant_next_y = ant_current_y
                elif ant_sensor_info[4] == "Obstacle":
                    reward = -20
                    ant_next_x = random.randint(0, 9)
                    ant_next_y = random.randint(0, 9)
                else:
                    reward = 2
                    ant_next_x = ant_current_x
                    ant_next_y = ant_current_y - 1

            rewards_in_this_episode += reward

            ant_current_x = ant_next_x
            ant_current_y = ant_next_y

            ant.ant_x = ant_current_x
            ant.ant_y = ant_current_y

        print("Rewards in this episode: " + str(rewards_in_this_episode))
        print("Count of times ant reached food in this episode: " + str(no_of_times_reached_food))
        print("Count of times ant clashed obstacle in this episode: " + str(no_of_times_clashed_obstacle))
        ant.rewards_per_episode.append(rewards_in_this_episode)
        if episode != 0 and episode % 10 == 0:
            ant.training_episode_value.append(episode)
            ant.training_reward_value.append(rewards_in_this_episode)
    running = False
    if not running:
        pygame.quit()

    test_average = mean(ant.rewards_per_episode)
    print("Test average: " + str(test_average))
    