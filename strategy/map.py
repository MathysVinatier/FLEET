import pygame
import numpy as np
import matplotlib.cm as cm
import Agent


class MAP():
    def __init__(self, width, height, matrix_size):
        self.MATRIX_SIZE = matrix_size
        self.WIDTH = width
        self.HEIGHT = height
        self.CELL_SIZE = self.WIDTH / self.MATRIX_SIZE

        self.matrix = self.generate_flora_density_matrix()
        self.surface = self.matrix_to_surface()
        self.fire_matrix = np.ones((self.MATRIX_SIZE, self.MATRIX_SIZE), dtype=int)
        
        self.add_habitation(5, 5, 5, 100)   # caserne
        self.add_habitation(50, 50, 5, 50)  # home
        self.add_habitation(60, 70, 5, 50)  # home
        self.add_habitation(50, 70, 5, 50)  # home

        pygame.init()
        

    def generate_flora_density_matrix(self):
        """ Generates the vegetation densities matrix (values between 0 and 1) """
        np.random.seed(42)  
        noise = np.random.rand(self.MATRIX_SIZE, self.MATRIX_SIZE)
        smooth_noise = np.copy(noise)
        for i in range(3):
            smooth_noise = (smooth_noise + np.roll(smooth_noise, 1, axis=0) + np.roll(smooth_noise, -1, axis=0) +
                            np.roll(smooth_noise, 1, axis=1) + np.roll(smooth_noise, -1, axis=1)) / 5
        return smooth_noise


    def matrix_to_surface(self):
        """ Transforms the matrix to a surface to display """
        color_map = cm.get_cmap('Greens')  
        surface = pygame.Surface((self.matrix.shape[1], self.matrix.shape[0]))
        for y in range(self.matrix.shape[0]):
            for x in range(self.matrix.shape[1]):
                value = self.matrix[y, x]   
                if value == 100:  
                    pygame_color = (139, 69, 19)  
                elif value == 50:
                    pygame_color = (128, 0, 128) 
                else:
                    color = color_map(value)
                    pygame_color = (int(color[0]*255), int(color[1]*255), int(color[2]*255))
                
                surface.set_at((x, y), pygame_color)
        return pygame.transform.scale(surface, (self.WIDTH, self.HEIGHT))

    
    def add_habitation(self, center_x, center_y, size, density_value=50):
        """ Adds a building given the coordinates of the center of the building and its size """
        half_size = size // 2 

        for i in range(center_x - half_size, center_x + half_size + 1):
            for j in range(center_y - half_size, center_y + half_size + 1):
                if 0 <= i < self.MATRIX_SIZE and 0 <= j < self.MATRIX_SIZE:
                    self.matrix[j, i] = density_value

        self.surface = self.matrix_to_surface()        


    def start_fire(self, x, y, size=1):
        """ Determines the zone of initial fire """
        half_size = size // 2
        for i in range(x - half_size, x + half_size + 1):
            for j in range(y - half_size, y + half_size + 1):
                if 0 <= i < self.MATRIX_SIZE and 0 <= j < self.MATRIX_SIZE:
                    self.fire_matrix[j, i] = 2 


    def draw_fire(self, screen):
        """ Changes the cells colors according to their state (1 : vegetation, 2 : fire, 3 : burnt) """
        for y in range(self.fire_matrix.shape[0]):
            for x in range(self.fire_matrix.shape[1]):
                if self.fire_matrix[y, x] == 2:
                    pygame.draw.rect(screen, (255, 0, 0), 
                                    (x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))
                elif self.fire_matrix[y, x] == 3:
                    pygame.draw.rect(screen, (105, 105, 105), 
                                    (x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))
                elif self.fire_matrix[y, x] == 4:
                    pygame.draw.rect(screen, (0, 0, 255), 
                                    (x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))


    def draw_map(self, screen):
        screen.blit(self.surface, (0, 0))




