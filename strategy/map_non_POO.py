import pygame
import numpy as np
import matplotlib.cm as cm
import random
import math

# ---- PARAMETRE DE LA CARTE ----- #
pairs = [(60, 600), (60, 450), (500, 30), (500, 60), (380,70), (20, 400)]
WIDTH, HEIGHT = 600, 600  
MATRIX_SIZE = 20  
CASERNE_SIZE = 200, 80
HOME_SIZE = 200, 80
X_ZONEH, Y_ZONEH = random.choice(pairs)
HOME_POS = 400 - 200//2, 400 - 80//2
WIND_SPEED = random.randint(0, 60)
WIND_ANGLE = random.randint(-180, 180)
FIRE_COLOR = (255, 0, 0)
FIRE_POS = (400, 400)
FIRE_RAD = 30
ROBOT_COLOR = (255, 220, 50)
ROBOT_SPEED = 0.2
ROBOT_RAD = 15
SAFE_DISTANCE = 40
WATER_COLOR = (0, 0, 255)
HOME_POS = (WIDTH - 400, HEIGHT - 10)

# ----- INITIALISATION ----- #
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Densité de Flore - Heatmap")

#fonction : générer une matrice avec une densité de flore
def generate_flora_density_matrix(size):
    np.random.seed(42)  
    noise = np.random.rand(size, size)  # Générer des valeurs entre 0 et 1
    smooth_noise = np.copy(noise)
    for i in range(3):  # Lisser la matrice
        smooth_noise = (smooth_noise + np.roll(smooth_noise, 1, axis=0) + np.roll(smooth_noise, -1, axis=0) +
                        np.roll(smooth_noise, 1, axis=1) + np.roll(smooth_noise, -1, axis=1)) / 5
    return smooth_noise

#fonction : Mapper la matrice vers des couleurs en nuances de vert
def matrix_to_surface(matrix, width, height):
    color_map = cm.get_cmap('Greens')  
    surface = pygame.Surface((matrix.shape[1], matrix.shape[0]))
    for y in range(matrix.shape[0]):
        for x in range(matrix.shape[1]):
            value = matrix[y, x]  
            color = color_map(value)  
            pygame_color = (int(color[0]*255), int(color[1]*255), int(color[2]*255))  # En RGB
            surface.set_at((x, y), pygame_color)
    return pygame.transform.scale(surface, (width, height))

# Charger l'image de la flèche (flèche pointant vers le haut)
arrow_image = pygame.image.load("strategy/images/blue-arrow-png.png")  # Remplacez par le chemin vers votre image
arrow_image = pygame.transform.scale(arrow_image, (80, 80))  # Redimensionner l'image de la flèche (facultatif)

# Fonction pour dessiner la flèche en fonction de l'angle
def draw_rotated_arrow(surface, x, y, angle=0):
    rotated_arrow = pygame.transform.rotate(arrow_image, angle)
    rotated_rect = rotated_arrow.get_rect(center=(x, y))  # Déplacer le centre de l'image à (x, y)   
    surface.blit(rotated_arrow, rotated_rect)

# Générer la matrice et la surface
flora_density = generate_flora_density_matrix(MATRIX_SIZE)
flora_surface = matrix_to_surface(flora_density, WIDTH, HEIGHT)

# Image PANNEAU 
image = pygame.image.load("strategy/images/France_road_sign_A24.svg.png")  # Remplacez par le chemin vers votre image

new_width = int(image.get_width() * 0.22)  # 50% de la largeur originale
new_height = int(image.get_height() * 0.22)  # 50% de la hauteur originale
resized_image = pygame.transform.scale(image, (new_width, new_height))

image_rect = resized_image.get_rect()  # Récupère les dimensions de l'image
font = pygame.font.Font(None, 36)


# IMAGE HOME
"""image_home = pygame.image.load("/Users/ecsrkhaif/Downloads/—Pngtree—fisherman house top view_9041534.png")  # Remplacez par le chemin vers votre image
image_home = pygame.transform.rotate(image_home, 90)
new_width_home = int(image_home.get_width() * 0.06)  # 50% de la largeur originale
new_height_home = int(image_home.get_height() * 0.06)  # 50% de la hauteur originale
resized_image_home = pygame.transform.scale(image_home, (new_width_home, new_height_home))
image_rect_home = resized_image_home.get_rect()  # Récupère les dimensions de l'image"""


### ------------ STRATEGIE -------------- ###
robot_size = 20
center_x, center_y = WIDTH // 2, HEIGHT // 2
target_pos = [400, 400]

robot_target_positions = [
    [target_pos[0] + (FIRE_RAD + SAFE_DISTANCE) * math.cos(math.radians(0)), target_pos[1] + (FIRE_RAD + SAFE_DISTANCE) * math.sin(math.radians(0))],
    [target_pos[0] + (FIRE_RAD + SAFE_DISTANCE) * math.cos(math.radians(120)), target_pos[1] + (FIRE_RAD + SAFE_DISTANCE) * math.sin(math.radians(120))],
    [target_pos[0] + (FIRE_RAD + SAFE_DISTANCE) * math.cos(math.radians(240)), target_pos[1] + (FIRE_RAD + SAFE_DISTANCE)* math.sin(math.radians(240))]
]
print("target robot : ", robot_target_positions)

robots = [
    {"pos": [30, 40],'target': robot_target_positions[0],"color": ROBOT_COLOR, "reached": False},  # Alpha
    {"pos": [100, 40], 'target': robot_target_positions[1],"color": ROBOT_COLOR,"reached": False},  # Beta
    {"pos": [170, 40], 'target': robot_target_positions[2],"color": ROBOT_COLOR,"reached": False},  # Gamma
]



def vitesse_de_prop(Influence_densité, Vitesse_Vent):
    V = Influence_densité * Vitesse_Vent
    return V

def angle_prop(Vitesse_prop, Vitesse_Vent):
    Influence_vent = Vitesse_prop/Vitesse_Vent
    alpha_min = 30 #deg
    alpha = alpha_min + 330 * (1 - Influence_vent) #330 car (360 - 30 des alpha min)
    return alpha #deg


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

def strat():
    return False 

### ------------ Boucle principale -------------- ###

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    for robot in robots:
        if not robot['reached']:
            robot['reached'] = move_robot(robot['pos'], robot['target'], ROBOT_SPEED)
            pygame.draw.line(screen,FIRE_COLOR, robot['pos'], target_pos)
    # Dessiner la heatmap
    screen.blit(flora_surface, (0, 0))
    
    # Dessiner la caserne
    rect_surface = pygame.Surface((CASERNE_SIZE), pygame.SRCALPHA)
    rect_surface.fill((255, 0, 0, 128))
    screen.blit(rect_surface, (0, 0))
    
    # Dessioner la zone habitable 
    rect_surface = pygame.Surface((CASERNE_SIZE), pygame.SRCALPHA)
    rect_surface.fill((0, 0, 255, 128))
    screen.blit(rect_surface, (X_ZONEH, Y_ZONEH))
    text_habit = font.render('Zone Habitable', True, (0, 0, 0))
    # Désinner la panneaux 
    image_rect.bottomright = (WIDTH - 10, HEIGHT - 35)
    screen.blit(resized_image, image_rect)
    
    
    text = font.render('Caserne', True, (0, 0, 0))
    text_s = str(WIND_SPEED) + ' km/h'
    text_SPEED = font.render(text_s, True, (0, 0, 0))
    screen.blit(text_habit, (X_ZONEH + 10, Y_ZONEH + HOME_SIZE[1]))
    screen.blit(text, (50, 80))
    screen.blit(text_SPEED, (WIDTH - 105, HEIGHT - 31))

    draw_rotated_arrow(screen, WIDTH - 165, HEIGHT - 62, angle=WIND_ANGLE)
    
    for robot in robots:
        pygame.draw.circle(screen, ROBOT_COLOR, robot['pos'], ROBOT_RAD)
        if robot['reached']:
            pygame.draw.line(screen, WATER_COLOR, 
                 robot['pos'],  # Utilisation du centre du robot sans ajout du rayon
                 (400, 400),  # Centre du feu
                 5)
    pygame.draw.circle(screen, FIRE_COLOR, FIRE_POS, FIRE_RAD)
    pygame.display.flip()

pygame.quit()

