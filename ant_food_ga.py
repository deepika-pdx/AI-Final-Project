import math
import random
from math import floor
import pygame as pg
from numpy.random import choice

# import pygame.event

# from ant2 import Ant
from Ant import Ant

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 800
ANT_SIZE = 30
should_quit = False
clock = pg.time.Clock()

food_position_x = SCREEN_WIDTH / 2
food_position_y = SCREEN_HEIGHT / 6
obstacle_position_x = SCREEN_WIDTH / 3
obstacle_position_y = SCREEN_HEIGHT / 2.5
obstacle_width = 0
obstacle_height = 0

ant_icon = pg.image.load("icons8-ant-30.png")
ant_population_count = 50
ant_list = []
ant_fitness_list = []
ant_lifespan = 40
no_of_generations = 300
new_ant_list = []
norm_ant_fitness_dict = {}


def generate_genes():
    angle = random.random() * 2 * math.pi
    x = random.randrange(0, 100) * math.cos(angle)
    y = random.randrange(0, 100) * math.sin(angle)
    return [x, y]


def generate_ant_population(count):
    for c in range(count):
        x_co_ordinate = random.randrange(ANT_SIZE, SCREEN_WIDTH - ANT_SIZE)
        y_co_ordinate = (random.randrange(SCREEN_HEIGHT - 100, SCREEN_HEIGHT)) - ANT_SIZE
        ant_genes = []
        for lifespan in range(ant_lifespan):
            ant_genes.append(generate_genes())

        generated_ant = Ant(x_co_ordinate, y_co_ordinate, ant_genes)
        ant_list.append(generated_ant)


def calculate_ant_fitness(individual_ant):
    food_pos = [food_position_x, food_position_y]
    ant_pos = [individual_ant.x_position, individual_ant.y_position]
    ant_fitness = math.dist(food_pos, ant_pos)
    return 1 / ant_fitness


def evaluate():
    calculated_ant_fitness_list = []
    # Determine the fitness of each ant
    for individual in ant_list:
        individual_fitness = calculate_ant_fitness(individual)
        if individual.reachedFood:
            individual_fitness = individual_fitness * 50
        elif individual.clashedObstacle:
            individual_fitness = individual_fitness / 100
        calculated_ant_fitness_list.append(individual_fitness)
    return calculated_ant_fitness_list


def normalise_ant_fitness():
    ant_index = 0
    pop_norm_ff_dict = {}
    # Normalise the fitness of each ant
    for ant_fitness in ant_fitness_list:
        normalised_ant_fitness = ant_fitness / sum(ant_fitness_list)
        pop_norm_ff_dict.update({ant_index: normalised_ant_fitness})
        ant_index += 1
    return pop_norm_ff_dict


def selection():
    next_gen_ants = []
    next_gen_ants_fitness = []
    parent_list = list(norm_ant_fitness_dict.keys())
    parent_fitness_list = list(norm_ant_fitness_dict.values())
    no_of_pairs = floor((len(parent_list) / 2))

    for i in range(no_of_pairs):
        parent_indices = choice(parent_list, 2, p=parent_fitness_list)
        while parent_indices[0] == parent_indices[1]:
            parent_indices[1] = random.choices(parent_list, weights=parent_fitness_list, k=1)[0]

        parent_one = ant_list[parent_indices[0]]
        parent_two = ant_list[parent_indices[1]]

        # Perform crossover and mutation
        child_array, child_fitness_array = crossover_and_mutation(parent_one, parent_two)
        next_gen_ants.append(child_array[0])
        next_gen_ants.append(child_array[1])

        next_gen_ants_fitness.append(child_fitness_array[0])
        next_gen_ants_fitness.append(child_fitness_array[1])

    return next_gen_ants, next_gen_ants_fitness


def crossover_and_mutation(parent_1, parent_2):
    child_ant_1_genes = []
    child_ant_2_genes = []
    ant_child_array = []
    ant_child_fitness_array = []

    # Performing crossover of the parent ant genes to generate two new child ant genes
    crossover_point = random.randint(1, floor(len(parent_1.genes) / 2))
    for m in range(len(parent_1.genes)):
        if m <= crossover_point:
            child_ant_1_genes.append(parent_1.genes[m])
            child_ant_2_genes.append(parent_2.genes[m])
        else:
            child_ant_1_genes.append(parent_2.genes[m])
            child_ant_2_genes.append(parent_1.genes[m])

    # Perform mutation based on probability
    should_mutate = choice([True, False], 1, p=[0.10, 0.90])

    if should_mutate:
        mutation_index_1 = random.randint(0, len(parent_1.genes) - 1)
        child_ant_1_genes[mutation_index_1] = generate_genes()

        mutation_index_2 = random.randint(0, len(parent_1.genes) - 1)
        child_ant_2_genes[mutation_index_2] = generate_genes()

    # child_1_x_co_ordinate = random.randrange(ANT_SIZE, SCREEN_WIDTH - ANT_SIZE)
    # child_1_y_co_ordinate = (random.randrange(SCREEN_HEIGHT - 100, SCREEN_HEIGHT)) - ANT_SIZE
    # child_2_x_co_ordinate = random.randrange(ANT_SIZE, SCREEN_WIDTH - ANT_SIZE)
    # child_2_y_co_ordinate = (random.randrange(SCREEN_HEIGHT - 100, SCREEN_HEIGHT)) - ANT_SIZE
    # generated_child_ant_1 = Ant(child_1_x_co_ordinate, child_1_y_co_ordinate, child_ant_1_genes)
    # generated_child_ant_2 = Ant(child_2_x_co_ordinate, child_2_y_co_ordinate, child_ant_2_genes)

    generated_child_ant_1 = Ant(parent_1.x_position + 2, parent_2.y_position - 4, child_ant_1_genes)
    generated_child_ant_2 = Ant(parent_2.x_position + 2, parent_1.y_position - 4, child_ant_2_genes)
    ant_child_array.append(generated_child_ant_1)
    ant_child_array.append(generated_child_ant_2)

    ant_child_1_fitness = calculate_ant_fitness(generated_child_ant_1)
    ant_child_2_fitness = calculate_ant_fitness(generated_child_ant_2)
    ant_child_fitness_array.append(ant_child_1_fitness)
    ant_child_fitness_array.append(ant_child_2_fitness)

    return ant_child_array, ant_child_fitness_array


def load_background():
    # Reloading the background
    window.blit(background, (0, 0))
    # Displaying the food
    food = pg.image.load("icons8-bread-loaf-48.png")
    window.blit(food, (food_position_x, food_position_y))
    # Displaying the obstacle
    obstacle = pg.image.load("brick_wall.png")
    obstacle_rect = obstacle.get_rect()
    obs_width = obstacle_rect.width
    obs_height = obstacle_rect.height
    window.blit(obstacle, (obstacle_position_x, obstacle_position_y))
    pg.display.update()
    return obs_width, obs_height


if __name__ == '__main__':
    pg.init()
    # Setting the background
    window = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Ant Food Hunting")
    background = pg.image.load("pexels-fwstudio-131634.jpg")

    # Generate the ant population
    generate_ant_population(ant_population_count)
    generation = 0
    for g in range(no_of_generations):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                should_quit = True
            else:
                generation += 1
                print("Generation number: " + str(generation))
                for lifespan_counter in range(ant_lifespan):
                    print("Lifespan count: " + str(lifespan_counter))
                    # Load the background
                    obstacle_width, obstacle_height = load_background()

                    font = pg.font.Font('freesansbold.ttf', 20)
                    text = font.render("Generation: " + str(generation), True, (255, 255, 255))
                    textRect = text.get_rect()
                    textRect.center = (80, 40)
                    window.blit(text, textRect)

                    # Display and start movement of the generated ants
                    for eachAnt in ant_list:
                        ant_x_coordinate = eachAnt.x_position
                        ant_y_coordinate = eachAnt.y_position
                        window.blit(ant_icon, (ant_x_coordinate, ant_y_coordinate))

                        # Calculate distance between ant current location and food
                        food_location = [food_position_x, food_position_y]
                        ant_location = [ant_x_coordinate, ant_y_coordinate]
                        ant_food_distance = math.dist(ant_location, food_location)

                        if ant_food_distance < 40:
                            eachAnt.reachedFood = True
                        #  print("Ant reached food")

                        if ((ant_x_coordinate > obstacle_position_x) and
                                (ant_x_coordinate < (obstacle_position_x + obstacle_width)) and
                                (ant_y_coordinate > obstacle_position_y) and
                                (ant_y_coordinate < (obstacle_position_y + obstacle_height))):
                            eachAnt.clashedObstacle = True
                        #   print("Ant clashed obstacle")

                        eachAnt.x_position += eachAnt.genes[lifespan_counter][0]
                        eachAnt.y_position -= eachAnt.genes[lifespan_counter][1]

                        if eachAnt.x_position > (SCREEN_WIDTH - ANT_SIZE):
                            eachAnt.x_position = random.randrange(ANT_SIZE, SCREEN_WIDTH - ANT_SIZE)
                        if eachAnt.y_position < ANT_SIZE:
                            eachAnt.y_position = (random.randrange(SCREEN_HEIGHT - 100, SCREEN_HEIGHT)) - ANT_SIZE

                        pg.display.update()
                    clock.tick(2)

                # Evaluation -->fitness
                ant_fitness_list = evaluate()
                norm_ant_fitness_dict = normalise_ant_fitness()
                # Selection --> select best and perform crossover and mutation--add them to new_ant_list
                new_ant_list, new_ant_fitness_list = selection()

                ant_list = new_ant_list
                ant_fitness_list = new_ant_fitness_list
                norm_ant_fitness_dict = normalise_ant_fitness()

    if should_quit:
        pg.quit()
