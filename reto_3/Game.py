import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Shooter Game')

# Colores
black = (0, 0, 0)

# Fondo
background_image = pygame.image.load('../reto_3/img/background.jpg')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Objetivo
target_image = pygame.image.load('../reto_3/img/target.jfif')
target_image_hit = pygame.image.load('../reto_3/img/target_hit.jfif')
target_image = pygame.transform.scale(target_image, (50, 50))  # Redimensionar imagen del objetivo
target_image_hit = pygame.transform.scale(target_image_hit, (50, 50))  # Redimensionar imagen del objetivo golpeado
target_rect = target_image.get_rect(center=(random.randint(50, screen_width - 50), random.randint(50, screen_height - 50)))

# Mira
crosshair_image = pygame.image.load('../reto_3/img/crosshair.png')
crosshair_image = pygame.transform.scale(crosshair_image, (50, 50))  # Redimensionar imagen de la mira
crosshair_rect = crosshair_image.get_rect()

# Bala
bullet_image = pygame.image.load('../reto_3/img/bullet.png')
bullet_image = pygame.transform.scale(bullet_image, (20, 10))  # Redimensionar imagen de la bala
bullet_speed = 10
bullets = []

# Función para mover el objetivo
def move_target():
    target_rect.center = (random.randint(50, screen_width - 50), random.randint(50, screen_height - 50))

# Función principal del juego
def main():
    global bullets
    running = True
    clock = pygame.time.Clock()
    target_hit = False
    target_hit_time = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if target_rect.collidepoint(event.pos):
                    target_hit = True
                    target_hit_time = pygame.time.get_ticks()
                    move_target()
                bullet_rect = bullet_image.get_rect(center=event.pos)
                bullets.append(bullet_rect)

        # Mover balas
        for bullet in bullets:
            bullet.y -= bullet_speed
        bullets = [bullet for bullet in bullets if bullet.y > 0]

        # Cambiar de imagen después de un breve período
        if target_hit and pygame.time.get_ticks() - target_hit_time > 500:
            target_hit = False

        # Obtener posición del mouse y actualizar la posición de la mira
        mouse_pos = pygame.mouse.get_pos()
        crosshair_rect.center = mouse_pos

        screen.blit(background_image, (0, 0))
        if target_hit:
            screen.blit(target_image_hit, target_rect)
        else:
            screen.blit(target_image, target_rect)

        # Dibujar balas
        for bullet in bullets:
            screen.blit(bullet_image, bullet)

        # Dibujar mira
        screen.blit(crosshair_image, crosshair_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
