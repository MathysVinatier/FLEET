import pygame


class Agent():
    def __init__(self, x, y, map):
        self.x = x
        self.y = y
        self.map = map
        self.image = pygame.image.load("strategy/images/robot.png")
        self.image = pygame.transform.scale(self.image, (self.map.CELL_SIZE, self.map.CELL_SIZE))
        self.radius = 0.5*self.map.CELL_SIZE

    def move(self, dx, dy):
        if self.x + dx <= self.map.WIDTH - 2:
            self.x += dx * self.map.CELL_SIZE
        if self.y + dy <= self.map.HEIGHT - 2:
            self.y += dy * self.map.CELL_SIZE

    def draw_agent(self, screen):
        #screen.blit(self.image, (self.x, self.y))
        pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), self.radius)
