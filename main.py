import pygame
import random
import math
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800,600))

background = pygame.image.load("background.jpg")
pygame.display.set_caption("space invaders")
icon = pygame.image.load("startup.png")
pygame.display.set_icon(icon)

score = 0
font = pygame.font.Font("freesansbold.ttf",32)
fontx = 10
fonty = 10

def display_score(x,y):
    sc = font.render("SCORE : "+str(score),True,(225,225,225))
    screen.blit(sc,(x,y))

playerImage = pygame.image.load("space-invaders.png")
playerx = 350
playery = 500
x_change = 0
y_change = 0

enemyImage =[]
enemyx =[]
enemyy =[]
enemy_x_change =[]
enemy_y_change = []
num_of_enemies =6

for i in range(num_of_enemies):
    enemyImage.append(pygame.image.load("monster.png"))
    enemyx.append(random.randint(0,800))
    enemyy.append(random.randint(0,50))
    enemy_x_change.append(0.3)
    enemy_y_change.append(40)

bullet_Image = pygame.image.load("bullet.png")
bulletx = 0
bullety = 480
bullet_y_change = 1
bullet_state = "ready"
# ready:cant see bullet yet,fire:appears

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_Image,(x+16,y+10))

def collision(ex,ey,bx,by):
    distance = math.sqrt(((ex-bx)**2)+((ey-by)**2))
    if distance<27:
        return True
    return False

def player(x,y):
    #blit : draw
    screen.blit(playerImage,(x,y))

def enemy(x,y,i):
    #blit : draw
    screen.blit(enemyImage[i],(x,y))

#music
mixer.music.load("background.mp3")
mixer.music.play(-1)

game_text = pygame.font.Font("freesansbold.ttf",64)
def game_over(x,y):
    text = game_text.render("GAME OVER",True,(225,225,225))
    screen.blit(text,(x,y))

running = True
while running:
    #screen.fill((0,28,66))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #keyboard,mouse events
        if event.type == pygame.KEYDOWN:
            print("key is pressed")
            if event.key == pygame.K_LEFT:
                x_change = -0.2
                print("left arrow is pressed")
            if event.key == pygame.K_RIGHT:
                x_change = 0.2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletx = playerx
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    fire_bullet(bulletx,bullety)
                print("space is pressed")
        if event.type == pygame.KEYUP :
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_change = 0
                print("left or right arrow is released")

    playerx+=x_change

    if playerx<=0:
        playerx = 736
    if playerx>=736:
        playerx = 0
    player(playerx,playery)

    for i in range(num_of_enemies):

        if enemyy[i]>400:
            for j in range(num_of_enemies):
                enemyy[j] = 1100
            game_over(200,300)
            break


        enemyx[i] +=enemy_x_change[i]
        if enemyx[i]<=0:
            enemy_x_change[i] = 0.3
            enemyy[i]+=enemy_y_change[i]
        if enemyx[i]>=768:
            enemyy[i]+=enemy_y_change[i]
            enemy_x_change[i] = -0.3

        colls = collision(enemyx[i], enemyy[i], bulletx, bullety)
        if colls:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bullety = 480
            bullet_state = "ready"
            score += 10
            print(score)
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(0, 50)
        enemy(enemyx[i],enemyy[i],i)

    if bullet_state == "fire":
        fire_bullet(bulletx,bullety)
        bullety-=bullet_y_change
    if bullety<=0:
        bullety = 480
        bullet_state = "ready"
    display_score(fontx,fonty)


    pygame.display.update()