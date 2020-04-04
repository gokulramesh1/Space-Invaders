import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load('background.png')

mixer.music.load('background.wav')
mixer.music.play(-1)

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

player_img = pygame.image.load('player.png')
player_x = 370
player_y = 480
player_x_change = 0

enemy_img = pygame.image.load('enemy.png')
num_of_enemies = 5
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = 30

for i in range(num_of_enemies):
    enemy_x.append(random.randint(100, 700))
    enemy_y.append(random.randint(10, 120))
    enemy_x_change.append(random.choice((4, -4)))

bullet_img = pygame.image.load('bullet.png')
bullet_x = []
bullet_y = []
bullet_x_change = 0
bullet_y_change = 10
num_of_bullets = 0

score_value = 0
score_font = pygame.font.Font('scorefont.ttf', 25)

over_font = pygame.font.Font('gameover.otf', 64)

explosion_img = pygame.image.load('explosion.png')

ammo_value = 50
ammo_font = pygame.font.Font('scorefont.ttf', 20)


def player(x, y):
    screen.blit(player_img, (x, y))


def enemies(x, y):
    for j in range(num_of_enemies):
        screen.blit(enemy_img, (x[j], y[j]))


def fire_bullet(x, y):
    screen.blit(bullet_img, (x + 20, y - 15))


def show_score():
    score = score_font.render(f"Score: {score_value}", True, (255, 255, 255))
    screen.blit(score, (10, 0))


def show_ammo():
    screen.blit(bullet_img, (720, 10))
    ammo = ammo_font.render(str(ammo_value), True, (255, 255, 255))
    screen.blit(ammo, (744, 5))


def game_over():
    go = over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(go, (226, 236))


def collision(enemy_x, enemy_y, bullet_x, bullet_y):
    x = (enemy_x + 32) - (bullet_x + 12)
    y = (enemy_y + 35) - (bullet_y)
    d = math.sqrt(x ** 2 + y ** 2)
    if d <= 30:
        return True
    return False


running = True

while running:

    screen.fill((0, 0, 0))  # RGB

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change -= 6
            if event.key == pygame.K_RIGHT:
                player_x_change += 6
            if event.key == pygame.K_SPACE:
                if ammo_value > 0:
                    bullet_x.append(player_x)
                    bullet_y.append(480)
                    num_of_bullets += 1
                    ammo_value -= 1
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    player_x += player_x_change

    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    for i in range(num_of_enemies):
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x[i] = 0
            enemy_x_change[i] *= -1
            enemy_y[i] += enemy_y_change
        elif enemy_x[i] >= 736:
            enemy_x[i] = 736
            enemy_x_change[i] *= -1
            enemy_y[i] += enemy_y_change

        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over()
            break

        j = 0
        while j < num_of_bullets:
            if collision(enemy_x[i], enemy_y[i], bullet_x[j], bullet_y[j]):
                screen.blit(explosion_img, (enemy_x[i], enemy_y[i]))
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                del bullet_x[j]
                del bullet_y[j]
                num_of_bullets -= 1
                score_value += abs(enemy_x_change[i]) + 1
                ammo_value += 1
                enemy_x[i] = random.randint(100, 700)
                enemy_y[i] = random.randint(10, 120)
                if enemy_x_change[i] > 0:
                    enemy_x_change[i] += 1
                else:
                    enemy_x_change[i] -= 1
            else:
                j += 1

    i = 0
    while i < num_of_bullets:
        fire_bullet(bullet_x[i], bullet_y[i])
        bullet_y[i] -= bullet_y_change
        if bullet_y[i] <= 0:
            del bullet_x[i]
            del bullet_y[i]
            num_of_bullets -= 1
        else:
            i += 1

    player(player_x, player_y)
    enemies(enemy_x, enemy_y)
    show_score()
    show_ammo()

    pygame.display.update()
