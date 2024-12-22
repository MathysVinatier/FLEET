import pygame
import random
import numpy as np
from Map import MAP

"""
INFLAMMABILITE 
- sens du vent
- densité

VITESSE CHANGEMENT COULEUR
- vitesse du vent
- niveau de densité
"""

class Feu():
    def __init__(self, map, wind_direction, wind_speed):
        self.map = map
        self.wind_direction = wind_direction
        self.wind_speed = wind_speed
        self.WIND_CRITICAL_THRESHOLD = 30
        self.RANDOMNESS_FACTOR = 0.5
        self.INFLAMMABILITY_TRESHOLD = 0.6
        self.COLORS = {
            0: (0, 0, 0),       # empty
            1: (34, 139, 34),   # vegetation  (green)
            2: (255, 0, 0),     # fire        (red)
            3: (105, 105, 105), # burnt       (grey)
            4: (0, 0, 255)      # water       (blue)
        }
        

    def calculate_wind_influence(self, dx, dy):
        """ Adds a weight according to the direction and speed of the wind """
        alignment = (dx * self.wind_direction[0] + dy * self.wind_direction[1]) / np.sqrt(dx**2 + dy**2)
        return max(0, alignment) * (self.wind_speed / 60)


    def propagate_fire(self):
        """ Calculates and updates the states of the fire matrix """
        new_fire_matrix = np.copy(self.map.fire_matrix)  

        for y in range(self.map.MATRIX_SIZE):
            for x in range(self.map.MATRIX_SIZE):
                # change fire cells to burnt cells
                if self.map.fire_matrix[y, x] == 2:  
                    new_fire_matrix[y, x] = 3 
                    # checking neighbors cells to propagate fire
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.map.MATRIX_SIZE and 0 <= ny < self.map.MATRIX_SIZE:
                                if self.map.fire_matrix[ny, nx] == 1:
                                    wind_influence = self.calculate_wind_influence(dx, dy)
                                    if self.wind_speed > self.WIND_CRITICAL_THRESHOLD and wind_influence <= 0:
                                        continue
                                    propagation_prob = self.map.matrix[ny, nx] * (1 + wind_influence) * (1 + self.RANDOMNESS_FACTOR * random.random())
                                    if propagation_prob > self.INFLAMMABILITY_TRESHOLD:
                                        new_fire_matrix[ny, nx] = 2  

        self.map.fire_matrix = new_fire_matrix


    