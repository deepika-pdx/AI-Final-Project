import random
import pygame as pg


class Ant:
    def __init__(self, x_pos, y_pos, genes=[]):
        self.x_position = x_pos
        self.y_position = y_pos
        self.fitness = 0
        self.reachedFood = False
        self.clashedObstacle = False
        self.genes = genes
