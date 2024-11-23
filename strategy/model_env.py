#--------------------------------------------------------#
#            Here it's the model for our env             #
#--------------------------------------------------------#
import pygame
import math


pygame.init()
# --- Couleur --- #
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WATER_COLOR = (0, 191, 255)  


WINDOW_SIZE = 600
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Trois Robots autour de la Cible")

"""---------- Parametres ---------"""

# Pos caserne
base_pos = [50, 50]
# Pos cible 
target_pos = [300, 300]

robot_size = 20
target_size = 20

robot_speed = 2

#Robot autour de la cible en x, y
circle_radius = 100
robot_target_positions = [
    [target_pos[0] + circle_radius * math.cos(math.radians(0)), target_pos[1] + circle_radius * math.sin(math.radians(0))],
    [target_pos[0] + circle_radius * math.cos(math.radians(120)), target_pos[1] + circle_radius * math.sin(math.radians(120))],
    [target_pos[0] + circle_radius * math.cos(math.radians(240)), target_pos[1] + circle_radius * math.sin(math.radians(240))]
]

# Pos init des robots (tous à la caserne)
robots = [
    {'pos': base_pos[:], 'target': robot_target_positions[0], 'reached': False},
    {'pos': base_pos[:], 'target': robot_target_positions[1], 'reached': False},
    {'pos': base_pos[:], 'target': robot_target_positions[2], 'reached': False}
]

"""---------------------------------"""

"""---------- Déplacement ---------"""
# -> Ici pour intégration de stratégie
def move_robot(robot_pos, target_pos, speed):
    dx = target_pos[0] - robot_pos[0]
    dy = target_pos[1] - robot_pos[1]
    distance = math.sqrt(dx**2 + dy**2)

    if distance > speed:
        dx /= distance
        dy /= distance
        robot_pos[0] += dx * speed
        robot_pos[1] += dy * speed
    else:
        return True  # pos atteinte
    return False

"""---------------------------------"""

"""---------- Main ---------"""
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # RAZ
    screen.fill(WHITE)

    # Robot -> cible
    for robot in robots:
        if not robot['reached']:
            robot['reached'] = move_robot(robot['pos'], robot['target'], robot_speed)

    # Dessin de la cible (cube rouge)
    pygame.draw.rect(screen, RED, (*target_pos, target_size, target_size))

    # Dessin de la caserne (point de départ des robots)
    pygame.draw.circle(screen, GREEN, base_pos, 10)

    #robot in new pos
    for robot in robots:
        pygame.draw.rect(screen, BLUE, (*robot['pos'], robot_size, robot_size))
        
        if robot['reached']:
            pygame.draw.line(screen, WATER_COLOR, 
                             (robot['pos'][0] + robot_size // 2, robot['pos'][1] + robot_size // 2), 
                             (target_pos[0] + target_size // 2, target_pos[1] + target_size // 2), 
                             5)  # Dessine une ligne épaisse (jet d'eau)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

"""---------------------------------"""
# Fermeture de Pygame
pygame.quit()