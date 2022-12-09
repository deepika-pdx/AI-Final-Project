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



environment_rows = 10
environment_columns = 10

q_values = np.zeros((environment_rows, environment_columns, 4))
#actions
actions = ['up', 'right', 'down', 'left']
# key_list = list(enumerate(actions))
# print(key_list)

rewards = np.full((environment_rows, environment_columns), -100)
rewards[2, 5] = 100

aisles = {}
aisles[1] = [i for i in range(1, 9)]
aisles[2] = [1, 2, 3, 4, 6, 7, 8]
aisles[3] = [1, 2, 8]
aisles[4] = [i for i in range(1, 9)]
aisles[5] = [i for i in range(1, 9)]
aisles[6] = [i for i in range(1, 9)]
aisles[7] = [i for i in range(1, 9)]
aisles[8] = [i for i in range(1, 9)]

for row_index in range(1, 9):
    for column_index in aisles[row_index]:
        rewards[row_index, column_index] = -1

for row in rewards:
    print(row)

def is_terminal_state(current_row_index, current_column_index):
  if rewards[current_row_index, current_column_index] == -1.:
    return False
  else:
    return True

def get_starting_location():
  current_row_index = np.random.randint(environment_rows)
  current_column_index = np.random.randint(environment_columns)
  while is_terminal_state(current_row_index, current_column_index):
    current_row_index = np.random.randint(environment_rows)
    current_column_index = np.random.randint(environment_columns)
  return current_row_index, current_column_index

def get_next_action(current_row_index, current_column_index, epsilon):
  if np.random.random() < epsilon:
    return np.argmax(q_values[current_row_index, current_column_index])
  else:
    return np.random.randint(4)

vel = 80
ant = Ant()
def get_next_location(current_row_index, current_column_index, action_index):
  new_row_index = current_row_index
  new_column_index = current_column_index
  if actions[action_index] == 'up' and current_row_index > 0 and ant.ant_y>0:
        new_row_index -= 1
        ant.ant_y -= vel
  elif actions[action_index] == 'right' and current_column_index < environment_columns - 1 and ant.ant_x <ant.window_x - ant.ant_size:
        new_column_index += 1
        ant.ant_x += vel
  elif actions[action_index] == 'down' and current_row_index < environment_rows - 1  and ant.ant_y < ant.window_y - ant.ant_size:
        new_row_index += 1
        ant.ant_y += vel
  elif actions[action_index] == 'left' and current_column_index > 0 and ant.ant_x > 0:
        new_column_index -= 1
        ant.ant_x -= vel
  return new_row_index, new_column_index


def get_shortest_path(start_row_index, start_column_index):
  if is_terminal_state(start_row_index, start_column_index):
    return []
  else:
    current_row_index, current_column_index = start_row_index, start_column_index
    shortest_path = []
    shortest_path.append([current_row_index, current_column_index])
    while not is_terminal_state(current_row_index, current_column_index):
      action_index = get_next_action(current_row_index, current_column_index, 1.)
      current_row_index, current_column_index = get_next_location(current_row_index, current_column_index, action_index)
      shortest_path.append([current_row_index, current_column_index])
    return shortest_path


epsilon = 0.9
discount_factor = 0.9
learning_rate = 0.2


#ant = Ant()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for episode in range(10):
        row_index, column_index = get_starting_location()

        while not is_terminal_state(row_index, column_index):
            action_index = get_next_action(row_index, column_index, epsilon)

            old_row_index, old_column_index = row_index, column_index
            row_index, column_index = get_next_location(row_index, column_index, action_index)

            reward = rewards[row_index, column_index]
            old_q_value = q_values[old_row_index, old_column_index, action_index]
            temporal_difference = reward + (discount_factor * np.max(q_values[row_index, column_index])) - old_q_value

            new_q_value = old_q_value + (learning_rate * temporal_difference)
            q_values[old_row_index, old_column_index, action_index] = new_q_value
#print('Training complete!')

    ant.display_ant()
    ant.display_wall()
    ant.display_bread()
    ant.draw_grid(ant.window_x, ant.window_y)
    pygame.display.update()

pygame.quit()


print(get_shortest_path(3, 8))
#print(get_shortest_path(5, 5))
#print(get_shortest_path(8, 5))

