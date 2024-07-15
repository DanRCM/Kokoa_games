import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Jumping Game')

# Cargar imagen de fondo
background_image = pygame.image.load('../reto_4/img/background.png')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Colores
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Jugador
player_image_ground = pygame.image.load('../reto_4/img/player.png')
player_image_ground = pygame.transform.scale(player_image_ground, (50, 50))  # Redimensionar imagen del jugador en el suelo
player_image_air = pygame.image.load('../reto_4/img/jumping_player.png')
player_image_air = pygame.transform.scale(player_image_air, (50, 50))  # Redimensionar imagen del jugador en el aire
player_image = player_image_ground
player_rect = player_image.get_rect(midbottom=(screen_width // 2, screen_height - 10))
player_speed_x = 5
player_speed_y = 0
gravity = 0.5
jump_power = -10
on_ground = True

# Plataformas
platform_image = pygame.image.load('../reto_4/img/platform.png')
platform_image = pygame.transform.scale(platform_image, (100, 20))  # Redimensionar imagen de la plataforma
platforms = [pygame.Rect(random.randint(0, screen_width - 100), screen_height - (i * 100), 100, 20) for i in range(6)]
platform_speed = 2

# Posicionar una plataforma en la mitad de la pantalla y al jugador sobre ella
mid_platform = pygame.Rect(screen_width // 2 - 50, screen_height // 2, 100, 20)
platforms.append(mid_platform)
player_rect.midbottom = mid_platform.midtop

# Puntos
point_image = pygame.image.load('../reto_4/img/point.jpg')
point_image = pygame.transform.scale(point_image, (20, 20))  # Redimensionar imagen del punto
points = [pygame.Rect(random.randint(0, screen_width - 20), random.randint(-screen_height, screen_height - 20), 20, 20) for _ in range(10)]
score = 0
font = pygame.font.Font(None, 36)

# Función para mostrar el puntaje
def draw_score():
    score_text = font.render(f'Score: {score}', 1, white)
    screen.blit(score_text, (10, 10))

# Función principal del juego
def main():
    global player_speed_y, score, player_image, on_ground
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed_x
        if keys[pygame.K_RIGHT] and player_rect.right < screen_width:
            player_rect.x += player_speed_x
        if keys[pygame.K_SPACE] and on_ground:
            player_speed_y = jump_power
            on_ground = False
            player_image = player_image_air  # Cambiar a la imagen de salto al saltar

        # Gravedad
        player_speed_y += gravity
        player_rect.y += player_speed_y

        # Colisiones con plataformas
        on_ground = False
        for platform in platforms:
            if player_rect.colliderect(platform) and player_speed_y > 0:
                player_rect.bottom = platform.top
                player_speed_y = 0
                on_ground = True
                player_image = player_image_ground  # Cambiar a la imagen de suelo al aterrizar

        # Mover plataformas
        for platform in platforms:
            platform.y += platform_speed
            if platform.top >= screen_height:
                platform.x = random.randint(0, screen_width - platform.width)
                platform.y = 0

        # Mover puntos
        for point in points:
            point.y += platform_speed
            if point.top >= screen_height:
                point.x = random.randint(0, screen_width - point.width)
                point.y = random.randint(-screen_height, 0)

        # Colisiones con puntos
        for point in points:
            if player_rect.colliderect(point):
                points.remove(point)
                points.append(pygame.Rect(random.randint(0, screen_width - 20), random.randint(-screen_height, screen_height - 20), 20, 20))
                score += 1

        # Perder el juego
        if player_rect.top > screen_height or any(platform.top > screen_height for platform in platforms):
            running = False

        # Dibujar elementos en pantalla
        screen.blit(background_image, (0, 0))
        screen.blit(player_image, player_rect)
        for platform in platforms:
            screen.blit(platform_image, platform)
        for point in points:
            screen.blit(point_image, point)
        draw_score()

        pygame.display.flip()
        clock.tick(60)

    # Mostrar mensaje de "Perdiste"
    screen.fill(black)
    game_over_text = font.render('Haz caido en las garras de tu ex', 1, red)
    final_score_text = font.render(f'Score final: {score}', 1, green)
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))
    screen.blit(final_score_text, (screen_width // 2 - final_score_text.get_width() // 2, screen_height // 2 + game_over_text.get_height()))
    pygame.display.flip()
    pygame.time.wait(3000)

    pygame.quit()

if __name__ == "__main__":
    main()