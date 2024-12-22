import pygame 
import numpy as np
import matplotlib.cm as cm
from scipy.spatial.distance import cdist

from Agent import Agent
from Map import MAP
from Feu import Feu



class Interface():
    def __init__(self, map_obj, robots, feu):
        self.map = map_obj
        self.robots = robots
        self.feu = feu
        self.priority_matrix = self.generate_priority_matrix()
        self.running = True

        self.robot_update_interval = 20 
        self.fire_update_interval = 200 
        self.last_robot_update = 0
        self.last_fire_update = 0

        self.SCREEN_WIDTH = self.map.WIDTH * 2
        self.SCREEN_HEIGHT = self.map.HEIGHT
        self.PRIORITY_MATRIX_WIDTH = self.map.WIDTH
        self.PRIORITY_MATRIX_HEIGHT = self.map.HEIGHT
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("<== FLEET ==>")


    def generate_priority_matrix(self):
        HOUSE_WEIGHT = 10
        DENSITY_WEIGHT = 0.5
        WIND_WEIGHT = 0.1
        DISTANCE_WEIGHT = 2
        priority_matrix = np.zeros((self.map.MATRIX_SIZE, self.map.MATRIX_SIZE))
        fire_positions = np.argwhere(self.map.fire_matrix == 2)

        for y in range(self.map.MATRIX_SIZE):
            for x in range(self.map.MATRIX_SIZE):

                # Adding priority of burnt cells
                if self.map.fire_matrix[y, x] == 3:
                    priority_matrix[y, x] = 0
                    continue

                # Adding priority of building
                if self.map.fire_matrix[y, x] == 50 or self.map.fire_matrix[y, x] == 100:
                    priority_matrix[y, x] += HOUSE_WEIGHT

                # Adding priority of density
                priority_matrix[y, x] += self.map.matrix[y, x] * DENSITY_WEIGHT

                # Adding priority of wind
                wind_influence = 0
                for fire_y, fire_x in fire_positions:
                    dx = x - fire_x
                    dy = y - fire_y
                    distance = np.sqrt(dx**2 + dy**2)
                    if distance == 0:
                        distance = 10e-5
                    wind_influence += self.feu.calculate_wind_influence(dx, dy) / distance
                priority_matrix[y, x] += wind_influence * WIND_WEIGHT

                # Adding priority of distance to the fire
                cell_position = np.array([[y, x]])
                distances = cdist(cell_position, fire_positions, metric='euclidean')
                min_distance = np.min(distances)
                distance_priority = max(0, DISTANCE_WEIGHT / (min_distance + 1))
                priority_matrix[y, x] += distance_priority
        
        return priority_matrix


    def draw_priority_matrix(self):
        color_map = cm.get_cmap('Reds')  
        surface = pygame.Surface((self.priority_matrix.shape[1], self.priority_matrix.shape[0]))
        for y in range(self.priority_matrix.shape[0]):
            for x in range(self.priority_matrix.shape[1]):
                value = self.priority_matrix[y, x]   
                color = color_map(value)
                pygame_color = (int(color[0]*255), int(color[1]*255), int(color[2]*255))
                surface.set_at((x, y), pygame_color)
        surface = pygame.transform.scale(surface, (self.PRIORITY_MATRIX_WIDTH, self.PRIORITY_MATRIX_HEIGHT))
        self.screen.blit(surface, (self.map.WIDTH, 0))


    def run(self):
        clock = pygame.time.Clock()
        pygame.time.delay(1000)
        while self.running:
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.map.draw_map(self.screen) 
            self.map.draw_fire(self.screen) 

            if current_time - self.last_fire_update >= self.fire_update_interval:
                self.feu.propagate_fire()
                self.last_fire_update = current_time
                self.priority_matrix = self.generate_priority_matrix()
                self.draw_priority_matrix()

            # if current_time - self.last_robot_update >= self.robot_update_interval:
            #     for robot in self.robots:
            #         robot.move(1, 1)                    
            #     self.last_robot_update = current_time       

            for robot in self.robots:
                robot.draw_agent(self.screen)

            pygame.display.flip()  
            clock.tick(60)  

        pygame.quit()


if __name__ == "__main__":
    map = MAP(750, 750, 75)
    cell_size = map.CELL_SIZE

    robot1 = Agent(cell_size*4.5, cell_size*4.5, map)
    robot2 = Agent(cell_size*6.5, cell_size*4.5, map)
    robot3 = Agent(cell_size*5.5, cell_size*6.5, map)

    feu = Feu(map, wind_direction=(1, 0), wind_speed=15)
    map.start_fire(30, 30, size=3)

    game = Interface(map, [robot1, robot2, robot3], feu)
    game.run()

    
