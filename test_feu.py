import pygame
import random
import numpy as np

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
        self.FPS = 0.5
        self.WIND_CRITICAL_THRESHOLD = 30
        self.RANDOMNESS_FACTOR = 0.3
        self.INFLAMMABILITY_TRESHOLD = 0.3
        self.CELL_SIZE = 30
        self.COLORS = {
            0: (0, 0, 0),      # empty
            1: (34, 139, 34),  # vegetation (green)
            2: (255, 0, 0),    # fire (red)
            3: (105, 105, 105) # burnt (grey)
        }

        pygame.init()
        self.screen = pygame.display.set_mode((self.map[0] * self.CELL_SIZE, self.map[1] * self.CELL_SIZE))
        pygame.display.set_caption("Simulation de Forêt en Feu")
        self.clock = pygame.time.Clock()
    

    def calculate_wind_influence(dx, dy, wind_direction, wind_speed):
        alignment = (dx * wind_direction[0] + dy * wind_direction[1]) / np.sqrt(dx**2 + dy**2)
        return max(0, alignment) * (wind_speed / 60)

    def run_simulation(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            new_forest = forest.copy()
            for y in range(self.map.shape[1]):
                for x in range(self.map.shape[0]):
                    if forest[y, x] == 2:  # En feu
                        new_forest[y, x] = 3  # Brûlé
                        for dy in range(-1, 2):
                            for dx in range(-1, 2):
                                nx, ny = x + dx, y + dy
                                if 0 <= nx < self.map.shape[0] and 0 <= ny < self.map.shape[1] and forest[ny, nx] == 1:
                                    # Influence du vent
                                    wind_influence = self.calculate_wind_influence(dx, dy, self.wind_direction, self.wind_speed)
                                    # Seuil critique
                                    if self.wind_speed > self.WIND_CRITICAL_THRESHOLD and wind_influence <= 0:
                                        continue
                                    # Probabilité de propagation
                                    propagation_prob = densities[ny, nx] * (1 + wind_influence) * (1 + self.RANDOMNESS_FACTOR * random.random())
                                    if propagation_prob > self.INFLAMMABILITY_TRESHOLD:  # Seuil d'inflammation
                                        new_forest[ny, nx] = 2

            forest = new_forest

            self.screen.fill((0, 0, 0))  # Fond noir
            for y in range(self.map.shape[1]):
                for x in range(self.map.shape[0]):
                    if forest[y, x] == 1:  # Végétation intacte
                        green_intensity = int(255 * densities[y, x])  # Calculer l'intensité du vert
                        color = (0, green_intensity, 0)  # Nuance de vert
                    else:
                        color = self.COLORS.get(forest[y, x], (0, 0, 0))  # Autres états (feu, brûlé, vide)
                    pygame.draw.rect(self, color, (x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))


        pygame.display.flip()
        self.clock.tick(self.FPS)


if __name__ == "__main__":
    pass