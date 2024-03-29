import asyncio
from random import randint

import pygame.image
import pygame.sprite as sprite
from pygame import Surface

import settings as config
from camera import Camera
from singleton import Singleton

chance = lambda x: not randint(0, x)


class Spring(sprite.Sprite):

    def __init__(self, parent: sprite.Sprite,
                 force=config.PLAYER_SPRING_JUMPFORCE):
        super().__init__()
        self.images = config.SPRING_IMAGES
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.parent = parent
        self.rect.midbottom = self.get_inital_pos()
        self.force = force
        self.jump_sound = pygame.mixer.Sound('sounds/feder.mp3')

    def get_inital_pos(self):
        x = randint(self.parent.rect.left + 20, self.parent.rect.right - 20)
        y = self.parent.rect.y + 3
        return x, y

    def onCollide(self):
        self.jump_sound.play()
        self.image = self.images[1]
        self.camera_rect = [self.camera_rect.x, self.camera_rect.y - 10]

    def draw(self, surface: Surface) -> None:
        self.camera_rect = Camera.instance.apply(self)
        surface.blit(self.image, self.camera_rect)


class Trampolin(sprite.Sprite):
    """
    A class to represent a bonus
    Inherits the Sprite class.
    """

    WIDTH = 45
    HEIGHT = 20

    def __init__(self, parent: sprite.Sprite,
                 force=config.PLAYER_TRAMP_JUMPFORCE):
        super().__init__()
        self.images = config.TRAMP_IMAGES
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.parent = parent
        self.rect.topleft = self.get_inital_pos()
        self.force = force
        self.jump_sound = pygame.mixer.Sound('sounds/tramp.mp3')

    def get_inital_pos(self):
        x = self.parent.rect.centerx - Trampolin.WIDTH // 2
        y = self.parent.rect.y - Trampolin.HEIGHT + 3
        return x, y

    def onCollide(self):
        self.jump_sound.play()

    def draw(self, surface: Surface) -> None:
        """ Render method,Should be called every frame after update.
        :param surface pygame.Surface: the surface to draw on.
        """
        # If camera instancied: calculate render positon
        self.camera_rect = Camera.instance.apply(self)
        surface.blit(self.image, self.camera_rect)


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y,
                 initial_spring=False, initial_tramp=False, breakable=False, moveable=False, monster=False):
        super().__init__()
        if breakable:
            self.image = config.PLATFORM_BREAKABLE_IMAGE
        elif moveable:
            self.image = config.PLATFORM_MOVEABLE_IMGAGE
        else:
            self.image = config.PLATFORM_BASE_IMAGE

        self.rect = self.image.get_rect()
        self.min_x = 0
        self.max_x = 0
        if moveable:
            pos_x = randint(0, (config.XWIN - config.PLATFORM_SIZE[0] - 200))
            self.min_x = pos_x
            self.max_x = randint(self.min_x + 200, config.XWIN)
            self.rect.topleft = [pos_x, pos_y]
        else:
            self.rect.topleft = [pos_x, pos_y]
        self.__level = Level.instance
        self.breakable = breakable
        self.moveable = moveable
        self.__bonus = None
        self.__type = None
        self.speed = 3
        self.jump_sound = pygame.mixer.Sound('sounds/jump.wav')
        self.break_sound = pygame.mixer.Sound('sounds/break.mp3')
        if initial_spring:
            self.add_bonus(Spring)
        if initial_tramp:
            self.add_bonus(Trampolin)
        if monster:
            self.add_bonus(Monstor)

    @property
    def bonus(self):
        return self.__bonus

    def move(self):

        if self.breakable:
            self.image = config.PLATFORM_BREAKABLE_IMAGE
        elif self.moveable:
            self.image = config.PLATFORM_MOVEABLE_IMGAGE
        else:
            self.image = config.PLATFORM_BASE_IMAGE

        if self.rect.right > self.max_x:
            self.speed *= -1
        if self.rect.left < self.min_x:
            self.speed *= -1
        self.rect.x += self.speed
        if self.__bonus is not None:
            self.__bonus.rect.x += self.speed

    def add_bonus(self, bonus_type: type) -> None:
        assert issubclass(bonus_type, (Spring, Trampolin, Monstor)), "Not a valid bonus type !"
        if not self.__bonus and not self.breakable:
            self.__bonus = bonus_type(self)

    def remove_bonus(self) -> None:
        self.__bonus = None

    def onCollide(self) -> None:
        if not self.breakable:
            self.jump_sound.play()
        if self.breakable:
            self.break_sound.play()
            self.__level.remove_platform(self)

    def draw(self, surface: Surface) -> None:

        if Camera.instance:
            self.camera_rect = Camera.instance.apply(self)
            surface.blit(self.image, self.camera_rect)
        #  pygame.draw.rect(surface, pygame.Color("blue"), self.camera_rect, 2)

        else:
            surface.blit(self.image, self.rect)
        # pygame.draw.rect(surface, pygame.Color("red"), self.rect, 2)

        if self.__bonus:
            self.__bonus.draw(surface)
        if self.camera_rect.y + self.rect.height > config.YWIN:
            self.__level.remove_platform(self)

    def update(self):
        if self.moveable:
            self.move()


class Monstor(sprite.Sprite):

    def __init__(self, parent: sprite.Sprite):
        super().__init__()
        self.images = config.SPRING_IMAGES
        self.image = config.MONSTER_IMAGE
        self.rect = self.image.get_rect()
        self.parent = parent
        self.rect.midbottom = self.get_inital_pos()
        self.mostor_sound = pygame.mixer.Sound('sounds/feder.mp3')
        self.health = randint(1, 3)

    def mostor_noise(self):
        self.mostor_sound.play()

    def get_inital_pos(self):
        x = self.parent.rect.centerx
        y = self.parent.rect.y
        return x, y

    def checkCollide(self, b:pygame.sprite.Group):
        return pygame.sprite.spritecollideany(self,b)


    def onCollide(self):
        pass

    def draw(self, surface: Surface) -> None:
        self.camera_rect = Camera.instance.apply(self)
        surface.blit(self.image, self.camera_rect)


class Level(Singleton, pygame.sprite.Group):
    """
    A class to represent the level.

    used to manage updates/generation of platforms.
    Can be access via Singleton: Level.instance.
    (Check Singleton design pattern for more info)
    """

    # constructor called on new instance: Level()
    def __init__(self):
        super().__init__()
        self.platform_size = config.PLATFORM_SIZE
        self.max_platforms = config.MAX_PLATFORM_NUMBER
        self.distance_min = min(config.PLATFORM_DISTANCE_GAP)
        self.distance_max = max(config.PLATFORM_DISTANCE_GAP)

        self.spring_platform_chance = config.SPRING_SPAWN_CHANCE
        self.tramp_platform_chance = config.TRAMP_SPAWN_CHANCE
        self.breakable_platform_chance = config.BREAKABLE_PLATFORM_CHANCE
        self.moveable_platform_chance = config.MOVEABLE_PLATFORM_CHANCE
        self.monster_chance = 40

        self.__platforms = []
        self.__to_remove = []

        self.__base_platform = Platform(
            config.HALF_XWIN - self.platform_size[0] // 2,  # X POS
            config.HALF_YWIN + config.YWIN / 3)

    # Public getter for __platforms so it remains private
    @property
    def platforms(self) -> list:
        return self.__platforms

    async def _generation(self) -> None:
        " Asynchronous management of platforms generation."
        # Check how many platform we need to generate
        nb_to_generate = self.max_platforms - len(self.__platforms)
        for _ in range(nb_to_generate):
            self.create_platform()

    def create_platform(self) -> None:
        " Create the first platform or a new one."
        if self.__platforms:
            # Generate a new random platform :
            # x position along screen width
            # y position starting from last platform y pos +random offset
            offset = randint(self.distance_min, self.distance_max)
            self.__platforms.append(Platform(
                randint(0, config.XWIN - self.platform_size[0]),
                self.__platforms[-1].rect.y - offset,
                initial_spring=chance(self.spring_platform_chance),
                initial_tramp=chance(self.tramp_platform_chance),
                breakable=chance(self.breakable_platform_chance),
                moveable=chance(self.moveable_platform_chance),
                monster=chance(self.monster_chance)
            ))
        else:
            # (just in case) no platform: add the base one
            self.__platforms.append(self.__base_platform)

    def remove_platform(self, plt: Platform) -> bool:
        """ Removes a platform safely.
        :param plt Platform: the platform to remove
        :return bool: returns true if platoform successfully removed
        """
        if plt in self.__platforms:
            self.__to_remove.append(plt)
            return True
        return False

    def reset(self) -> None:
        " Called only when game restarts (after player death)."
        self.__platforms = [self.__base_platform]

    def update(self) -> None:
        " Should be called each frame in main game loop for generation."
        for platform in self.__platforms:
            self.add(platform)
            platform.update()
        for platform in self.__to_remove:
            if platform in self.__platforms:
                self.__platforms.remove(platform)
                self.remove(platform)
        self.__to_remove = []
        asyncio.run(self._generation())

    def draw(self, surface: Surface) -> None:
        """ Called each frame in main loop, draws each platform
        :param surface pygame.Surface: the surface to draw on.
        """
        for platform in self.__platforms:
            platform.draw(surface)
