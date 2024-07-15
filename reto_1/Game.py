import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Colores
black = (0, 0, 0)
white = (255, 255, 255)

# Dimensiones de las paletas
paddle_width = 15
paddle_height = 90

# Configuración de las paletas
paddle_speed = 5
left_paddle = pygame.Rect(50, (screen_height - paddle_height) // 2, paddle_width, paddle_height)
right_paddle = pygame.Rect(screen_width - 50 - paddle_width, (screen_height - paddle_height) // 2, paddle_width,
                           paddle_height)

# Configuración de la pelota
ball_size = 20
ball = pygame.Rect(screen_width // 2 - ball_size // 2, screen_height // 2 - ball_size // 2, ball_size, ball_size)
ball_speed_x = 5 * random.choice((1, -1))
ball_speed_y = 4 * random.choice((1, -1))

# Marcadores
left_score = 0
right_score = 0
font = pygame.font.Font(None, 74)


# Función para mostrar el marcador
def draw_score():
    left_text = font.render(str(left_score), 1, white)
    right_text = font.render(str(right_score), 1, white)
    screen.blit(left_text, (screen_width // 4, 10))
    screen.blit(right_text, (screen_width * 3 // 4, 10))


# Función principal del juego
def main():
    global ball, ball_speed_x, ball_speed_y, left_score, right_score

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= paddle_speed
        if keys[pygame.K_s] and left_paddle.bottom < screen_height:
            left_paddle.y += paddle_speed
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= paddle_speed
        if keys[pygame.K_DOWN] and right_paddle.bottom < screen_height:
            right_paddle.y += paddle_speed

        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= screen_height:
            ball_speed_y *= -1

        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_speed_x *= -1

        if ball.left <= 0:
            right_score += 1
            ball = pygame.Rect(screen_width // 2 - ball_size // 2, screen_height // 2 - ball_size // 2, ball_size,
                               ball_size)
            ball_speed_x *= random.choice((1, -1))
            ball_speed_y *= random.choice((1, -1))

        if ball.right >= screen_width:
            left_score += 1
            ball = pygame.Rect(screen_width // 2 - ball_size // 2, screen_height // 2 - ball_size // 2, ball_size,
                               ball_size)
            ball_speed_x *= random.choice((1, -1))
            ball_speed_y *= random.choice((1, -1))

        screen.fill(black)
        pygame.draw.rect(screen, white, left_paddle)
        pygame.draw.rect(screen, white, right_paddle)
        pygame.draw.ellipse(screen, white, ball)
        pygame.draw.aaline(screen, white, (screen_width // 2, 0), (screen_width // 2, screen_height))

        draw_score()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
