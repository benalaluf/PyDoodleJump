from math import copysign

import pygame
from pygame._sprite import collide_rect
from pygame.constants import *
from pygame.math import Vector2
from pygame.event import Event

import level
from singleton import Singleton
from sprite import Sprite
from level import Level
import settings as config

# Return the sign of a number: getsign(-5)-> -1
getsign = lambda x: copysign(1, x)


class Player(Sprite, Singleton):
    def __init__(self, *args):
        Sprite.__init__(self, *args)
        self.__startrect = self.rect.copy()
        self.__maxvelocity = Vector2(config.PLAYER_MAX_SPEED, 100)
        self.__startspeed = 1.5

        self._velocity = Vector2()
        self._input = 0
        self._jumpforce = config.PLAYER_JUMPFORCE
        self._bonus_jumpforce = config.PLAYER_SPRING_JUMPFORCE

        self.gravity = config.GRAVITY
        self.accel = .5
        self.deccel = .6
        self.dead = False

    def _fix_velocity(self) -> None:
        self._velocity.y = min(self._velocity.y, self.__maxvelocity.y)
        self._velocity.y = round(max(self._velocity.y, -self.__maxvelocity.y), 2)
        self._velocity.x = min(self._velocity.x, self.__maxvelocity.x)
        self._velocity.x = round(max(self._velocity.x, -self.__maxvelocity.x), 2)

    def reset(self) -> None:
        self._velocity = Vector2()
        self.rect = self.__startrect.copy()
        self.camera_rect = self.__startrect.copy()
        self.dead = False

    def handle_event(self, event: Event) -> None:
        # Check if start moving
        if event.type == KEYDOWN:
            # Moves player only on x-axis (left/right)
            if event.key == K_LEFT or event.key == K_a:
                self._velocity.x = -self.__startspeed
                self._input = -1
                self.set_image(config.PLAYER_IMAGE_LEFT)

            elif event.key == K_RIGHT or event.key == K_d:
                self._velocity.x = self.__startspeed
                self._input = 1
                self.set_image(config.PLAYER_IMAGE_RIGHT)
        # Check if stop moving
        elif event.type == KEYUP:
            if (event.key == K_LEFT or event.key == K_a and self._input == -1) or (
                    event.key == K_RIGHT or event.key == K_d and self._input == 1):
                self._input = 0

    def jump(self, force: float = None) -> None:
        if not force: force = self._jumpforce
        self._velocity.y = -force

    def onCollide(self, obj: Sprite) -> None:
        self.rect.bottom = obj.rect.top
        self.jump()

    def onCollideNoJump(self, obj: Sprite) -> None:
        self.rect.bottom = obj.rect.top

    def collisions(self) -> None:
        lvl = Level.instance
        if not lvl: return
        for platform in lvl.platforms:
            # check falling and colliding <=> isGrounded ?
            if self._velocity.y > .5:
                # check collisions with platform's spring bonus
                if platform.bonus and collide_rect(self, platform.bonus):
                    platform.bonus.onCollide()
                    self.onCollide(platform.bonus)
                    self.jump(platform.bonus.force)

                # check collisions with platform
                if collide_rect(self, platform):
                    if platform.breakable:
                        self.onCollideNoJump(platform)
                    else:
                        self.onCollide(platform)
                    platform.onCollide()

    def update(self) -> None:
        if self.camera_rect.y > config.YWIN * 2:
            self.dead = True
            return
        self._velocity.y += self.gravity
        if self._input:  # accelerate
            self._velocity.x += self._input * self.accel
        elif self._velocity.x:  # deccelerate
            self._velocity.x -= getsign(self._velocity.x) * self.deccel
            self._velocity.x = round(self._velocity.x)
        self._fix_velocity()

        self.rect.x = (self.rect.x + self._velocity.x) % (config.XWIN - self.rect.width)
        self.rect.y += self._velocity.y

        self.collisions()
