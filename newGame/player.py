from math import copysign

import pygame.sprite
from pygame import *
from pygame.event import Event
import settings as config
from newGame.camera import Camera
from newGame.level import Level
import math as math

getsign = lambda x: copysign(1, x)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = config.PLAYER_IMAGE_RIGHT
        self.rect = self.image.get_rect()
        self.rect.topleft = [config.HALF_XWIN - config.PLAYER_SIZE[0] / 2,  # X POS
                             config.HALF_YWIN + config.HALF_YWIN / 2]
        self.gunshoot_sound = pygame.mixer.Sound('sounds/lasser.wav')
        self.oriention = [True, False]

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

        self.lastkeypressed = ['d']

        self.camera_rect = self.rect.copy()

        self.bullets = []
        self.__to_remove = []
        self.time = False
        self.start_time = 0

    def shoot(self, x=None, y=None):
        self.gunshoot_sound.play()
        if x is None or y is None:
            x, y = pygame.mouse.get_pos()
        print(self.rect.x, self.rect.y)
        self.bullets.append(
            Bullet(x, y, self.camera_rect.centerx, self.camera_rect.y)
        )

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
                self.oriention[0] = False
                self.lastkeypressed.append('a')

            elif event.key == K_RIGHT or event.key == K_d:
                self._velocity.x = self.__startspeed
                self._input = 1
                self.oriention[0] = True
                self.lastkeypressed.append('d')

            elif event.key == K_UP or event.key == K_w:
                self.image = config.PLAYER_IMAGE_LEFT
                self.lastkeypressed.append('w')
                self.shoot(x=self.camera_rect.centerx, y=self.camera_rect.y - 100)

        elif event.type == KEYUP:
            if (event.key == K_LEFT or event.key == K_a and self._input == -1) or (
                    event.key == K_RIGHT or event.key == K_d and self._input == 1):
                self._input = 0
            if self.lastkeypressed[len(self.lastkeypressed) - 1] == 'w':
                self.lastkeypressed.pop()
                if self.lastkeypressed[len(self.lastkeypressed) - 1] == 'd':
                    self.image = config.PLAYER_IMAGE_RIGHT
                elif self.lastkeypressed[len(self.lastkeypressed) - 1] == 'a':
                    self.image = config.PLAYER_IMAGE_LEFT

    def jump(self, force: float = None) -> None:
        self.oriention[1] = True
        if not force: force = self._jumpforce
        self._velocity.y = -force

    def onCollide(self, other_rect) -> None:
        self.start_time = pygame.time.get_ticks()
        self.rect.bottom = other_rect.rect.top
        self.jump()

    def collisions(self) -> None:
        lvl = Level.instance
        if not lvl: return
        for platform in lvl.platforms:
            # check falling and colliding <=> isGrounded ?
            if self._velocity.y > .5:
                # check collisions with platform's spring bonus
                if platform.bonus and self.rect.colliderect(platform.bonus.rect):
                    platform.bonus.onCollide()
                    self.onCollide(platform.bonus)
                    self.jump(platform.bonus.force)

                # check collisions with platform
                if self.rect.colliderect(platform.rect):
                    if abs(platform.rect.top - self.rect.bottom) < 30:
                        if platform.breakable:
                            pass
                        else:
                            self.onCollide(platform)
                        platform.onCollide()

    def update_oriention(self):
        if self.oriention[0]:
            if self.oriention[1]:
                self.image = config.PLAYER_IMAGE_JUMP_RIGHT
            else:
                self.image = config.PLAYER_IMAGE_RIGHT
        else:
            if self.oriention[1]:
                self.image = config.PLAYER_IMAGE_JUMP_LEFT
            else:
                self.image = config.PLAYER_IMAGE_LEFT
        if pygame.time.get_ticks() - self.start_time > 400:
            self.oriention[1] = False

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

        # orientaion
        self.update_oriention()

        for b in self.bullets:
            b.move()
        for bullet in self.__to_remove:
            if bullet in self.bullets:
                self.bullets.remove(bullet)
        self.__to_remove = []

        self.collisions()

    def remove_bullet(self, blt) -> bool:
        """ Removes a platform safely.
        :param plt Platform: the platform to remove
        :return bool: returns true if platoform successfully removed
        """
        if blt in self.bullets:
            self.__to_remove.append(blt)
            return True
        return False

    def draw(self, surface: Surface) -> None:
        """ Render method,Should be called every frame after update.
        :param surface pygame.Surface: the surface to draw on.
        """
        # If camera instancied: calculate render positon
        if Camera.instance:
            self.camera_rect = Camera.instance.apply(self)
            surface.blit(self.image, self.camera_rect)
        # pygame.draw.rect(surface, pygame.Color("blue"), self.camera_rect, 2)

        else:
            surface.blit(self.image, self.rect)
        #   pygame.draw.rect(surface, pygame.Color("red"), self.rect, 2)
        for bullet in self.bullets:
            bullet.draw(surface)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, targetx, targety, pos_x, pos_y):
        super().__init__()
        self.image = config.BULLET_IMAGE
        self.rect = self.image.get_rect()
        angle = math.atan2(targety - pos_y, targetx - pos_x)  # get angle to target in radians
        # print('Angle in degrees:', int(angle * 180 / math.pi))
        self.speed = 30
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.camera_rect = self.rect.copy()

    def move(self):
        # self.x and self.y are floats (decimals) so I get more accuracy
        # if I change self.x and y and then convert to an integer for
        # the rectangle.
        self.pos_x = self.pos_x + self.dx
        self.pos_y = self.pos_y + self.dy
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y

    # Override
    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)
        if self.camera_rect.y + self.rect.height > config.YWIN:
            Player.instance.remove_bullet(self)
