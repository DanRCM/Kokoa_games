import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invaders')

# Colores
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Fondo
background_image = pygame.image.load('../reto_2/img/images.jfif')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Jugador
player_image = pygame.image.load('../reto_2/img/player.png')
player_image = pygame.transform.scale(player_image, (50, 50))  # Redimensionar imagen del jugador
player_rect = player_image.get_rect(midbottom=(screen_width // 2, screen_height - 10))
player_speed = 5

# Enemigos
enemy_image = pygame.image.load('../reto_2/img/enemy.png')
enemy_image = pygame.transform.scale(enemy_image, (40, 40))  # Redimensionar imagen del enemigo
special_enemy_image = pygame.image.load('../reto_2/img/special_enemy.png')
special_enemy_image = pygame.transform.scale(special_enemy_image, (40, 40))  # Redimensionar imagen del enemigo especial
enemy_width = enemy_image.get_width()
enemy_height = enemy_image.get_height()
enemy_speed = 1.5
enemy_direction = 1
enemies = [pygame.Rect(x * 60, y * 60, enemy_width, enemy_height) for x in range(10) for y in range(3)]
special_enemies = [pygame.Rect(random.randint(0, screen_width - enemy_width), random.randint(0, screen_height // 2), enemy_width, enemy_height) for _ in range(5)]

# Balas
bullet_image = pygame.image.load('../reto_2/img/bullet.png')
bullet_image = pygame.transform.scale(bullet_image, (10, 20))  # Redimensionar imagen de la bala
bullet_width = bullet_image.get_width()
bullet_height = bullet_image.get_height()
bullet_speed = 7
bullets = []
enemy_bullets = []
enemy_bullet_speed = 5

# Función para mover al jugador
def move_player(keys, player_rect):
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < screen_width:
        player_rect.x += player_speed

# Función para disparar una bala
def shoot_bullet(player_rect):
    bullet_rect = bullet_image.get_rect(midbottom=(player_rect.centerx, player_rect.top))
    bullets.append(bullet_rect)

# Función para mover las balas
def move_bullets(bullets, speed):
    for bullet in bullets:
        bullet.y += speed
    bullets[:] = [bullet for bullet in bullets if 0 < bullet.y < screen_height]

# Función para mover a los enemigos
def move_enemies(enemies):
    global enemy_direction
    move_down = False
    for enemy in enemies:
        enemy.x += enemy_speed * enemy_direction
        if enemy.right >= screen_width or enemy.left <= 0:
            move_down = True

    if move_down:
        enemy_direction *= -1
        for enemy in enemies:
            enemy.y += 10

# Función para mover enemigos especiales en múltiples direcciones
def move_special_enemies(special_enemies):
    for special_enemy in special_enemies:
        special_enemy.x += random.choice([-1, 1]) * enemy_speed
        special_enemy.y += random.choice([-1, 1]) * enemy_speed
        if special_enemy.left <= 0 or special_enemy.right >= screen_width:
            special_enemy.x -= random.choice([-1, 1]) * enemy_speed
        if special_enemy.top <= 0 or special_enemy.bottom >= screen_height // 2:
            special_enemy.y -= random.choice([-1, 1]) * enemy_speed

# Función para detectar colisiones
def check_collisions(bullets, enemies, special_enemies, player_rect):
    for bullet in bullets:
        for enemy in enemies:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                return
        for special_enemy in special_enemies:
            if bullet.colliderect(special_enemy):
                bullets.remove(bullet)
                special_enemies.remove(special_enemy)
                return
    for bullet in enemy_bullets:
        if bullet.colliderect(player_rect):
            enemy_bullets.remove(bullet)
            print("Game Over!")
            pygame.quit()

# Función para que los enemigos disparen
def enemy_shoot(enemies):
    if random.random() < 0.01:  # Probabilidad de disparo
        enemy = random.choice(enemies)
        bullet_rect = bullet_image.get_rect(midbottom=(enemy.centerx, enemy.bottom))
        enemy_bullets.append(bullet_rect)

# Función principal del juego
def main():
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot_bullet(player_rect)
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        move_player(keys, player_rect)
        move_bullets(bullets, -bullet_speed)
        move_bullets(enemy_bullets, enemy_bullet_speed)
        move_enemies(enemies)
        move_special_enemies(special_enemies)
        check_collisions(bullets, enemies, special_enemies, player_rect)
        enemy_shoot(enemies + special_enemies)

        screen.blit(background_image, (0, 0))  # Dibujar imagen de fondo
        screen.blit(player_image, player_rect)
        for bullet in bullets:
            screen.blit(bullet_image, bullet)
        for enemy in enemies:
            screen.blit(enemy_image, enemy)
        for special_enemy in special_enemies:
            screen.blit(special_enemy_image, special_enemy)
        for bullet in enemy_bullets:
            screen.blit(bullet_image, bullet)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
