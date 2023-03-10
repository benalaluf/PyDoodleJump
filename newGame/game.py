import random

import pygame, sys

# General SetUp
from newGame.camera import Camera
from newGame.level import Platform, Level
from newGame.player import Player

pygame.init()
clock = pygame.time.Clock()

# Game Screen
screen_width = 640
screen_height = 1024
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load('images/background.png')

# Camera
Camera()

# Player
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

# Platfor
platform_group = Level()

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
    platform_group.update()
    player_group.draw(screen)
    player_group.update()
    clock.tick(120)
