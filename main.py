import pygame
from pygame import mixer
import random
import math

#Initialize pygame 
pygame.init()

#Create window
screen = pygame.display.set_mode((800, 600))

#Title and icon
pygame.display.set_caption("Space invaders")
icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)

#Background
background = pygame.image.load("images/background.jpg")

#Sound
#mixer.music.load("images/background.wav")
#mixer.music.play(-1)

#Player
playerImg = pygame.image.load("images/player.png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
directions = [-1, 1]

for i in range(num_of_enemies) :
    enemyImg.append(pygame.image.load("images/alien-ship.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(random.choice(directions))
    enemyY_change.append(40)

    
#Bullet

#Ready - You can't see bullet on screen
#Fire - bullet is currently moving
bulletImg = pygame.image.load("images/bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 3
bullet_state = "ready"


#puts player on surface
def player(x, y):
    screen.blit(playerImg, (x, y))

#puts enemy on surface
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_Bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16,y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27 :
        return True
    else :
        return False

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 20)
textX = 10
textY = 10
def show_score(x,y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x,y))

#Game over Text
over_font = pygame.font.Font("freesansbold.ttf", 64)

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

#Game loop
running = True
while running :
    screen.fill((0, 0, 0))
    #background image
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change = -2
            if event.key == pygame.K_d:
                playerX_change = 2
            if event.key == pygame.K_w:
                playerY_change = -2
            if event.key == pygame.K_s:
                playerY_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound("images/laser.wav")
                    bullet_Sound.play()
                    bulletY = playerY
                    bulletX = playerX
                    fire_Bullet(bulletX, bulletY)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0
            if event.key == pygame.K_w or event.key == pygame.K_s :
                playerY_change = 0
    

    playerY += playerY_change
    playerX += playerX_change      

    #Boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    if playerY <= 300:
        playerY = 300
    elif playerY >= 536:
        playerY = 536

    #Enemy movement
    for i in range(num_of_enemies):
        #Game Over
        enemy_distance = math.sqrt(math.pow(enemyX[i] - playerX, 2) + math.pow(enemyY[i] - playerY, 2))
        if enemy_distance < 30 or enemy_distance > 1000:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break 

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

         #Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision : 
            explosion_Sound = mixer.Sound("images/explosion.wav")
            explosion_Sound.play()
            bulletY = playerY
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(0, 150)
            enemyX_change[i] = random.choice(directions)
        enemy(enemyX[i], enemyY[i], i)

    #Bullet Movement
    if bulletY <= 0:
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_Bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    

    #Update surface
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
