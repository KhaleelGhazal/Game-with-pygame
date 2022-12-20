import math
import random
import pygame

from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
background = pygame.image.load("background.png")
mixer.music.load("background.wav")
mixer.music.play(-1)

pygame.display.set_caption("SPACE ENEMIES")
icon = pygame.image.load("flag.png")
pygame.display.set_icon(icon)
playerImage = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

alienImage = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
alien_count = 5

for i in range(alien_count):
    alienImage.append(pygame.image.load("alien.png"))
    alienX.append(random.randint(0, 736))
    alienY.append(random.randint(50, 150))
    alienX_change.append(4)
    alienY_change.append(40)

bulletImage = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "un-show"

score_value = 0
font = pygame.font.Font("PinkAcapella.otf", 32)

testX = 10
testY = 10

GameOverFont = pygame.font.Font("PinkAcapella.otf", 64)


def show_score(x, y):
    score = font.render("score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = GameOverFont.render("YOU SUCK!", True, (255, 255, 255))
    screen.blit(over_text, (300, 250))


def player(x, y):
    screen.blit(playerImage, (x, y))


def alien(x, y, i):
    screen.blit(alienImage[i], (x, y))


def shoot(x, y):
    global bullet_state
    bullet_state = "show"
    screen.blit(bulletImage, (x+16, y+10))


def collisionCheck(alienX, alienY, bulletX, bulletY):
    distance = math.sqrt(math.pow(alienX-bulletX, 2) + (math.pow(alienY-bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "un-show":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    shoot(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerY >= 736:
        playerY = 736

    for i in range(alien_count):
        if alienY[i] > 440:
            for j in range(alien_count):
                alienY[j] = 2000
            game_over_text()
            break
        alienX[i] += alienX_change[i]
        if alienX[i] <= 0:
            alienX_change[i] = 4
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 736:
            alienX_change[i] = -4
            alienY[i] += alienY_change[i]

        collision = collisionCheck(alienX[i], alienY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "un-show"
            score_value += 1
            alienX[i] = random.randint(0,736)
            alienY[i] = random.randint(50,150)

        alien(alienX[i], alienY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "un-show"
    if bullet_state == "show":
        shoot(bulletX, bulletY)
        bulletY -= bulletY_change
    player(playerX, playerY)
    show_score(testX, testY)
    pygame.display.update()
