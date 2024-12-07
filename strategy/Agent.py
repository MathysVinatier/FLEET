import pygame


class Agent():
    def __init__(self, x, y, map):
        self.x = x
        self.y = y
        self.image = pygame.image.load("strategy/images/robot.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.map = map
        self.radius = 0.5*self.map.CELL_SIZE

    def move(self, dx, dy):
        self.x = max(0, min(self.x + dx, self.map.WIDTH - self.image.get_width()))
        self.y = max(0, min(self.y + dy, self.map.HEIGHT - self.image.get_height()))

    def draw_agent(self, screen):
        #screen.blit(self.image, (self.x, self.y))
        pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), self.radius)
