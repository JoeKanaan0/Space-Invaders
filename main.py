import pygame
pygame.font.init()
from pygame import mixer
pygame.mixer.init()
import os

# window
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
WHITE = (255, 255, 255)

# background
BACKGROUND_IMAGE = pygame.image.load("background.png")
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))
mixer.music.load("background.wav")
mixer.music.play(-1)

# player
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 60
PLAYER_SPEED = 7
PLAYER_IMAGE = pygame.image.load("player.png")
PLAYER = pygame.transform.scale(PLAYER_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT))

# bullet
BULLET_WIDTH = 5
BULLET_HEIGHT = 10
RED = (255, 0, 0)
BULLET_SPEED = 10

# enemies
ENEMY_WIDTH = 60
ENEMY_HEIGHT = 50
ENEMY_IMAGE = pygame.image.load("enemy.png")
ENEMY = pygame.transform.scale(ENEMY_IMAGE, (ENEMY_WIDTH, ENEMY_HEIGHT))
ENEMY_SPEED = 5
ENEMY2_SPEED = 7
ENEMY3_SPEED = 9
UFO_WIDTH = 40
UFO_HEIGHT = 30
UFO_IMAGE = pygame.image.load("ufo.png")
UFO = pygame.transform.scale(UFO_IMAGE, (UFO_WIDTH, UFO_HEIGHT))
UFO_SPEED = 13
UFO2_SPEED = 9

# score
SCORE = pygame.font.SysFont('comicsans', 40)
ENEMY_HIT = pygame.USEREVENT + 1
ENEMY2_HIT = pygame.USEREVENT + 2
ENEMY3_HIT = pygame.USEREVENT + 5
UFO_HIT = pygame.USEREVENT + 3
UFO2_HIT = pygame.USEREVENT + 4
LOST_FONT = pygame.font.SysFont('comicsans', 100)


def handle_bullets(max_bullets, enemy, ufo, enemy2, ufo2, enemy3):
    for bullet in max_bullets:
        bullet.y -= BULLET_SPEED
        if bullet.y < 0:
            max_bullets.remove(bullet)
        if enemy.colliderect(bullet):
            max_bullets.remove(bullet)
            enemy.x = WIDTH - ENEMY_WIDTH
            enemy.y = ENEMY_HEIGHT*2
            pygame.event.post(pygame.event.Event(ENEMY_HIT))
        elif ufo.colliderect(bullet):
            max_bullets.remove(bullet)
            ufo.x = 0
            ufo.y = ENEMY_HEIGHT*3
            pygame.event.post(pygame.event.Event(UFO_HIT))
        elif enemy2.colliderect(bullet):
            max_bullets.remove(bullet)
            enemy2.x = 0
            enemy2.y = ENEMY_HEIGHT*3
            pygame.event.post(pygame.event.Event(ENEMY2_HIT))
        elif ufo2.colliderect(bullet):
            max_bullets.remove(bullet)
            ufo2.x = 0
            ufo2.y = ENEMY_HEIGHT*3 
            pygame.event.post(pygame.event.Event(UFO2_HIT))
        elif enemy3.colliderect(bullet):
            max_bullets.remove(bullet)
            enemy3.x = 0
            enemy3.y = ENEMY_HEIGHT*3
            pygame.event.post(pygame.event.Event(ENEMY3_HIT))
        

def enemyship(enemy):
    if enemy.x > 0:
        enemy.x -= ENEMY_SPEED
    else:
        enemy.x = WIDTH - ENEMY_WIDTH
        enemy.y = enemy.y + ENEMY_HEIGHT

def enemy2ship(enemy2):
    if enemy2.x < WIDTH - ENEMY_WIDTH:
        enemy2.x += ENEMY2_SPEED
    else:
        enemy2.x = 0
        enemy2.y = enemy2.y + ENEMY_HEIGHT


def ufoship(ufo):
    if ufo.x < WIDTH - UFO_WIDTH:
        ufo.x += UFO_SPEED
    else:
        ufo.x = 0
        ufo.y = ufo.y + ENEMY_HEIGHT

def ufo2ship(ufo2):
    if ufo2.x < WIDTH - UFO_WIDTH:
        ufo2.x += UFO2_SPEED
    else:
        ufo2.x = 0
        ufo2.y = ufo2.y + ENEMY_HEIGHT   

def enemy3ship(enemy3):
    if enemy3.x < WIDTH - UFO_WIDTH:
        enemy3.x += ENEMY3_SPEED
    else:
        enemy3.x = 0
        enemy3.y = enemy3.y + ENEMY_HEIGHT     

def movement(player, keys_pressed):
    if keys_pressed[pygame.K_a] and player.x > 0:
        player.x -= PLAYER_SPEED
    if keys_pressed[pygame.K_d] and player.x + PLAYER_WIDTH < WIDTH:
        player.x += PLAYER_SPEED
    if keys_pressed[pygame.K_w] and player.y > 0:
        player.y -= PLAYER_SPEED
    if keys_pressed[pygame.K_s] and player.y + PLAYER_HEIGHT < HEIGHT:
        player.y += PLAYER_SPEED

def draw(player, max_bullets, enemy, ufo, enemy2, points, ufo2, enemy3):
    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(PLAYER, (player.x, player.y))
    WIN.blit(ENEMY, (enemy.x, enemy.y))
    WIN.blit(UFO, (ufo.x, ufo.y))
    WIN.blit(ENEMY, (enemy2.x, enemy2.y))
    WIN.blit(UFO, (ufo2.x, ufo2.y))
    WIN.blit(ENEMY, (enemy3.x, enemy3.y))
    score = SCORE.render("Score: " + str(points), 1, WHITE)
    WIN.blit(score, (10, 10))
    for bullet in max_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()

def lost(text):
    draw_text = LOST_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    player = pygame.Rect(WIDTH//2 - PLAYER_WIDTH//2, HEIGHT - PLAYER_HEIGHT*2, PLAYER_WIDTH, PLAYER_HEIGHT)
    ufo = pygame.Rect(0, UFO_HEIGHT*3, UFO_WIDTH, UFO_HEIGHT)
    ufo2 = pygame.Rect(WIDTH//2 - UFO_WIDTH//2, UFO_HEIGHT * 6, UFO_WIDTH, UFO_HEIGHT)
    enemy = pygame.Rect(WIDTH - ENEMY_WIDTH, ENEMY_HEIGHT*2, ENEMY_WIDTH, ENEMY_HEIGHT)
    enemy2 = pygame.Rect(0, ENEMY_HEIGHT*3, ENEMY_WIDTH, ENEMY_HEIGHT)
    enemy3 = pygame.Rect(WIDTH - ENEMY_WIDTH, ENEMY_HEIGHT*4, ENEMY_WIDTH, ENEMY_HEIGHT)
    clock = pygame.time.Clock()
    running = True
    max_bullets = []
    points = 0

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            elif event.type == pygame.KEYDOWN:
               if event.key == pygame.K_SPACE and len(max_bullets) < 3:
                     bullet = pygame.Rect(player.x + PLAYER_WIDTH//2 - BULLET_WIDTH//2, player.y - BULLET_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT )
                     max_bullets.append(bullet)
                     bullet_Sound = mixer.Sound('laser.wav')
                     bullet_Sound.play()

            if event.type == ENEMY_HIT:
                points += 1
                explosion_Sound = mixer.Sound('explosion.wav')
                explosion_Sound.play()

            if event.type == ENEMY2_HIT:
                points += 2
                explosion_Sound = mixer.Sound('explosion.wav')
                explosion_Sound.play()

            if event.type == UFO_HIT:
                points += 5
                explosion_Sound = mixer.Sound('explosion.wav')
                explosion_Sound.play()

            if event.type == UFO2_HIT:
                points += 4
                explosion_Sound = mixer.Sound('explosion.wav')
                explosion_Sound.play()
            
            if event.type == ENEMY3_HIT:
                points += 3
                explosion_Sound = mixer.Sound('explosion.wav')
                explosion_Sound.play()

        
        losing_text = ""
        if enemy.y + ENEMY_HEIGHT*2 > HEIGHT or enemy2.y + ENEMY_HEIGHT*2 > HEIGHT or ufo.y + ENEMY_HEIGHT*2 > HEIGHT or ufo2.y + ENEMY_HEIGHT*2 > HEIGHT or enemy.y + ENEMY_HEIGHT*2 > HEIGHT:
            losing_text = "You Lost!"
        if enemy.colliderect(player) or enemy2.colliderect(player) or ufo.colliderect(player) or ufo.colliderect(player) or enemy3.colliderect(player):
            losing_text = "You Lost!"
        if losing_text != "":
            lost(losing_text)
            main()
            
        keys_pressed = pygame.key.get_pressed()
        draw(player, max_bullets, enemy, ufo, enemy2, points, ufo2, enemy3)
        movement(player, keys_pressed)
        handle_bullets(max_bullets, enemy, ufo, enemy2, ufo2, enemy3)
        enemyship(enemy)
        enemy2ship(enemy2)
        enemy2ship(enemy2)
        ufoship(ufo)
        ufo2ship(ufo2)
        enemy3ship(enemy3)

        pygame.display.update()

if __name__ == "__main__":
    main()