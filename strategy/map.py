import pygame
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as mcolors



class MAP():
    def __init__(self, width, height, matrix_size):
        self.MATRIX_SIZE = matrix_size
        self.WIDTH = width
        self.HEIGHT = height
        self.matrix = self.generate_flora_density_matrix()
        self.surface = self.matrix_to_surface()

        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Densité de Flore - Heatmap")


    def generate_flora_density_matrix(self):
        np.random.seed(42)  
        noise = np.random.rand(self.MATRIX_SIZE, self.MATRIX_SIZE)
        smooth_noise = np.copy(noise)
        for i in range(3):  # Lisser la matrice
            smooth_noise = (smooth_noise + np.roll(smooth_noise, 1, axis=0) + np.roll(smooth_noise, -1, axis=0) +
                            np.roll(smooth_noise, 1, axis=1) + np.roll(smooth_noise, -1, axis=1)) / 5
        return smooth_noise


    def matrix_to_surface(self):
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
        half_size = size // 2 

        for i in range(center_x - half_size, center_x + half_size + 1):
            for j in range(center_y - half_size, center_y + half_size + 1):
                if 0 <= i < self.MATRIX_SIZE and 0 <= j < self.MATRIX_SIZE:
                    self.matrix[j, i] = density_value

        self.surface = self.matrix_to_surface()


    def draw_map(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.add_habitation(5, 5, 5, 100)  # caserne
            self.add_habitation(50, 50, 5, 50) # home
            self.add_habitation(70, 70, 5, 50) # home 
            self.add_habitation(50, 70, 5, 50) # home
            self.screen.blit(self.surface, (0, 0))
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    m = MAP(600, 600, 100)
    m.draw_map()



