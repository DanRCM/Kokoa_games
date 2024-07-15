import pygame
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego similar a agar.io")

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Configuraciones del círculo principal
player_pos = [WIDTH // 2, HEIGHT // 2]
player_radius = 20
player_speed = 5

# Configuraciones de los pequeños círculos
small_circles = []
max_small_circles = 10
small_circle_radius = 5

# Función para generar pequeños círculos
def generate_small_circles():
    for _ in range(max_small_circles):
        x = random.randint(small_circle_radius, WIDTH - small_circle_radius)
        y = random.randint(small_circle_radius, HEIGHT - small_circle_radius)
        small_circles.append([x, y])

generate_small_circles()

# Función para detectar colisiones
def check_collision(circle1_pos, circle1_radius, circle2_pos, circle2_radius):
    distance = ((circle1_pos[0] - circle2_pos[0]) ** 2 + (circle1_pos[1] - circle2_pos[1]) ** 2) ** 0.5
    return distance < circle1_radius + circle2_radius

# Bucle principal del juego
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Obtener la posición del ratón
    mouse_pos = pygame.mouse.get_pos()

    # Movimiento del círculo principal con el teclado
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP]:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed

    # Movimiento del círculo principal hacia el ratón
    player_pos[0] += (mouse_pos[0] - player_pos[0])*0.1
    player_pos[1] += (mouse_pos[1] - player_pos[1])*0.1

    # Dibujo del círculo principal
    pygame.draw.circle(screen, BLUE, (int(player_pos[0]), int(player_pos[1])), player_radius)

    # Dibujo y actualización de los pequeños círculos
    for circle in small_circles[:]:
        pygame.draw.circle(screen, RED, (circle[0], circle[1]), small_circle_radius)
        if check_collision(player_pos, player_radius, circle, small_circle_radius):
            small_circles.remove(circle)
            player_radius += 1

    # Generar nuevos pequeños círculos si hay menos de max_small_circles
    if len(small_circles) < max_small_circles:
        generate_small_circles()

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()