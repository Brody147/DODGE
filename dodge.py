from random import randint
import pygame
from pygame import *
pygame.init()


score = -1

FPS = 60
clock = pygame.time.Clock()

speed = 6

x = 100
y = 100
x_vel = 0
y_vel = 0


class Enemy():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_vel = 0
        self.y_vel = 0
        self.speed = 1

    def update(self):

        self.x += self.x_vel * self.speed
        self.y += self.y_vel * self.speed

        self.x_vel *= 0.94

        if self.x < 0:
            global enemy1, enemy2, enemy3, enemy1_rect, enemy2_rect, enemy3_rect
            enemy1, enemy2, enemy3, enemy1_rect, enemy2_rect, enemy3_rect = wave()
            return (self.x, self.y)

        return (self.x, self.y)

    def left(self):
        self.x_vel -= 1

    def right(self):
        self.x_vel += 1

    def up(self):
        self.y_vel -= 1

    def down(self):
        self.y_vel += 1


WIN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("DODGE!")

IMG = pygame.transform.scale(
    (pygame.image.load("asset\\transparent.png")), (100, 100))

enemy_img = pygame.transform.scale(
    (pygame.image.load("asset\\enemy.png")), (100, 100))


def wave():

    global score
    score += 1

    while True:
        enemy1 = Enemy(1280 - 100, randint(0, 720 - 100))
        enemy2 = Enemy(1280 - 100, randint(0, 720 - 100))
        enemy3 = Enemy(1280 - 100, randint(0, 720 - 100))

        enemy1_rect = pygame.Rect(enemy1.x, enemy1.y, 100, 100)
        enemy2_rect = pygame.Rect(enemy2.x, enemy2.y, 100, 100)
        enemy3_rect = pygame.Rect(enemy3.x, enemy3.y, 100, 100)

        if (not enemy1_rect.colliderect(enemy2_rect) and
            not enemy1_rect.colliderect(enemy3_rect) and
                not enemy2_rect.colliderect(enemy3_rect)):
            break

    return (enemy1, enemy2, enemy3, enemy1_rect, enemy2_rect, enemy3_rect)


enemy1, enemy2, enemy3, enemy1_rect, enemy2_rect, enemy3_rect = wave()

while True:

    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("asset\\music.mp3")
        pygame.mixer.music.play()

    keys = pygame.key.get_pressed()
    if keys[K_a] or keys[K_LEFT]:
        x_vel -= 1
    if keys[K_d] or keys[K_RIGHT]:
        x_vel += 1
    if keys[K_w] or keys[K_UP]:
        y_vel -= 1
    if keys[K_s] or keys[K_DOWN]:
        y_vel += 1

    # Move enemies left continuously
    enemy1.left()
    enemy2.left()
    enemy3.left()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    x_vel *= 0.8
    y_vel *= 0.8

    x += x_vel * speed
    y += y_vel * speed

    if x < 0:
        x = 0
    if x > 1280 - 100:
        x = 1280 - 100
    if y < 0:
        y = 0
    if y > 720 - 100:
        y = 720 - 100

    WIN.fill((100, 36, 0))

    WIN.blit(IMG, (x, y))

    WIN.blit(enemy_img, enemy1.update())
    WIN.blit(enemy_img, enemy2.update())
    WIN.blit(enemy_img, enemy3.update())

    enemy1_rect.topleft = (enemy1.x, enemy1.y)
    enemy2_rect.topleft = (enemy2.x, enemy2.y)
    enemy3_rect.topleft = (enemy3.x, enemy3.y)

    player_rect = pygame.Rect(x + 17, y + 25, 60, 60)

    if (player_rect.colliderect(enemy1_rect) or
        player_rect.colliderect(enemy2_rect) or
            player_rect.colliderect(enemy3_rect)):
        pygame.quit()

    font = pygame.font.SysFont(None, 48)
    score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
    WIN.blit(score_surf, (10, 10))

    clock.tick(FPS)

    pygame.display.update()
