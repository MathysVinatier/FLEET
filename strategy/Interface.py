import pygame 
from Agent import Agent
from Map import MAP
from Feu import Feu


class Interface():
    def __init__(self, map_obj, robots, feu):
        self.map = map_obj
        self.robots = robots
        self.feu = feu
        self.running = True

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.map.draw_map() 
            self.feu.propagate_fire()  
            self.map.draw_fire() 

            for robot in self.robots:
                robot.draw_agent(self.map.screen)

            pygame.display.flip()  
            clock.tick(5)  

        pygame.quit()


if __name__ == "__main__":
    map = MAP(600, 600, 100)
    cell_size = map.CELL_SIZE

    robot1 = Agent(cell_size*4.5, cell_size*4.5, map)
    robot2 = Agent(cell_size*6.5, cell_size*4.5, map)
    robot3 = Agent(cell_size*5.5, cell_size*6.5, map)

    feu = Feu(map, wind_direction=(1, 0), wind_speed=5)
    map.start_fire(30, 30, size=3)

    game = Interface(map, [robot1, robot2, robot3], feu)
    game.run()
