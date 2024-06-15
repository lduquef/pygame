import pygame
import time
from functions import Button, Player, Bullet, objects, screen, Enemy

# Inicialización de Pygame y configuración inicial del juego
pygame.init()
width, height = 800, 600
pygame.display.set_caption("Fly-Shooter-Game")
clock = pygame.time.Clock()

# Definición de botones en la pantalla
Button(150, 450, 200, 100, 'Jugar')
Button(450, 450, 200, 100, 'Créditos')
Button(680, 10, 90, 45, "Menú")

img_flecha= pygame.transform.scale(pygame.image.load('assets/flechas.png').convert_alpha(), (130, 200))
# Carga y redimensionamiento de imágenes del personaje
img_sprite = [
    pygame.transform.scale(pygame.image.load('assets/Fly (1).png').convert_alpha(), (150, 100)),
    pygame.transform.scale(pygame.image.load('assets/Fly (2).png').convert_alpha(), (150, 100))
]

# Carga y redimensionamiento de imágenes de enemigos
img_enemies = [
    pygame.transform.scale(pygame.image.load(f'assets/enemy{i+1}.png').convert_alpha(), (120, 100))
    for i in range(3)
]

# Carga de imágenes de fondo
fill = pygame.image.load('assets/BG.png')
credits_bg = pygame.transform.scale(pygame.image.load('assets/credits.png').convert(), (width, height))

# Carga de imagen del bullet
bullet_img = pygame.transform.scale(pygame.image.load('assets/Bullet (1).png').convert_alpha(), (30, 30))

# Variables de juego
Player1 = Player()
enemy = Enemy()
bullets = []
last_shot_time = time.time()
value = 0

# Bucle principal del juego
running = True
while running:
    clock.tick(60)
    screen.blit(fill, [0, 0])
    screen.blit(img_flecha, [335, 200])
    # Procesamiento de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                Player1.up()
            if event.key == pygame.K_DOWN:
                Player1.down()

    # Verificación de estado de botones
    if objects[2].alreadyPressed:  # Botón de menú
        objects[0].alreadyPressed = False
        objects[1].alreadyPressed = False
    elif objects[1].alreadyPressed:  # Estado del botón de créditos
        screen.blit(credits_bg, [0, 0])  # Mostrar fondo de créditos
    elif not objects[0].alreadyPressed:
        for obj in objects:  # Procesar otros botones
            obj.process()
    elif objects[0].alreadyPressed:  # Estado del botón de jugar
        Player1.gravity()
        screen.blit(fill, [0, 0])  # Mostrar fondo de juego
        enemy.move()

    # Inicializar la imagen del enemigo con la primera imagen de la lista
        enemy_image = img_enemies[0]

        # Detección de colisiones entre balas y enemigo
        bullets_to_remove = []
        for bullet in bullets:
            bullet.move()
            bullet.draw(screen)
            
            # Verificar colisión entre balas y enemigo
            if bullet.position[0] < enemy.position[0] + enemy.size[0] and \
               bullet.position[0] + bullet.size[0] > enemy.position[0] and \
               bullet.position[1] < enemy.position[1] + enemy.size[1] and \
               bullet.position[1] + bullet.size[1] > enemy.position[1]:
                enemy.hit()  # Reducir la vida del enemigo
                bullets_to_remove.append(bullet)
    # Eliminar las balas que colisionaron con el enemigo
        for bullet in bullets_to_remove:
            bullets.remove(bullet)


        # Disparar balas cada 0.2 segundos
        current_time = time.time()
        if current_time - last_shot_time > 0.2:
            bullet = Bullet(Player1.position[0] + Player1.size[0] * 5, Player1.position[1] + Player1.size[1] * 2, bullet_img)
            bullets.append(bullet)
            last_shot_time = current_time

        # Cambiar la imagen del enemigo según su vida
        if enemy.health < 40:
            enemy_image = img_enemies[2]
        elif enemy.health < 80:
            enemy_image = img_enemies[1]
        else:
            enemy_image = img_enemies[0]

        # Alternar disfraces del jugador
        value = value % 2
        Player1.draw(screen, img_sprite[value])
        enemy.draw(screen, enemy_image)
        # Dibujar barra de vida del enemigo
        pygame.draw.rect(screen, (255, 0, 0), (enemy.position[0], enemy.position[1] - 10, enemy.health, 5))
        # Verificar si la vida del enemigo llegó a cero
        if enemy.health <= 0:
            running = False  # Detener el juego si el enemigo está muerto
    objects[2].process()  # Procesar botón Home siempre disponible
    value += 1
    pygame.display.flip()
