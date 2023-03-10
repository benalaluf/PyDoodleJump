from math import copysign
import math

import pygame.sprite
from pygame import *
from pygame.event import Event
import settings as config
from newGame.level import Level

getsign = lambda x: copysign(1, x)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = config.PLAYER_IMAGE_RIGHT
        self.rect = self.image.get_rect()
        self.rect.topleft = [config.HALF_XWIN - config.PLAYER_SIZE[0] / 2,  # X POS
                             config.HALF_YWIN + config.HALF_YWIN / 2]
        self.gunshoot_sound = pygame.mixer.Sound('sounds/lasser.wav')

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

    def shoot(self):
        self.gunshoot_sound.play()
        x, y = pygame.mouse.get_pos()
        print(self.rect.x, self.rect.y)
        self.bullets.append(
            Player.Bullet(self.rect.centerx, self.rect.y, x, y)
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
                self.image = (config.PLAYER_IMAGE_LEFT)
                self.lastkeypressed.append('a')

            elif event.key == K_RIGHT or event.key == K_d:
                self._velocity.x = self.__startspeed
                self._input = 1
                self.image = (config.PLAYER_IMAGE_RIGHT)
                self.lastkeypressed.append('d')

            elif event.key == K_UP or event.key == K_w:
                self.image = config.PLAYER_IMAGE_LEFT
                self.lastkeypressed.append('w')
                b = Player.Bullet(self.rect.centerx, self.rect.y, self.rect.centerx, self.rect.centery - 1000)
                self.bullets.append(b)

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
        if not force: force = self._jumpforce
        self._velocity.y = -force

    def onCollide(self, other_rect) -> None:
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
                    #if abs(platform.rect.top - self.rect.bottom) < 4:
                        if platform.breakable:
                            pass
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

        for bullet in self.__to_remove:
            if bullet in self.bullets:
                self.bullets.remove(bullet)
        self.__to_remove = []

        for b in self.bullets:
            b.move()

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

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw(surface)

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, targetx, targety, pos_x, pos_y):
            super().__init__()
            self.image = pygame.image.load('images/doodle_r.png')
            self.rect = self.image.get_rect()
            angle = math.atan2(targety - pos_y, targetx - pos_x)  # get angle to target in radians
            # print('Angle in degrees:', int(angle * 180 / math.pi))
            self.speed = 1
            self.dx = math.cos(angle) * self.speed
            self.dy = math.sin(angle) * self.speed
            self.pos_x = pos_x
            self.pos_y = pos_y
            self.camera_rect = self.rect.copy()
            self.player = Player.instance

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
                self.player.remove_bullet(self)
