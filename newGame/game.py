import random

import pygame, sys

# General SetUp
from newGame.level import Platform
from newGame.player import Player

pygame.init()
clock = pygame.time.Clock()

# Game Screen
screen_width = 640
screen_height = 1024
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load('images/background.png')


# Player
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

# Platform
platform_group = pygame.sprite.Group()
for platform in range(20):
    new_platform = Platform('images/baseplatform.png',random.randint(0, screen_width), random.randint(0, screen_height))
    platform_group.add(new_platform)

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.shoot()

    pygame.display.flip()
    screen.blit(background, (0, 0))
    platform_group.draw(screen)
    player_group.draw(screen)
    player_group.update()
    clock.tick(120)
