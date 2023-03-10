from random import randint

import pygame.image
import pygame.sprite as sprite
from pygame import Surface

import settings as config
from newGame.singleton import Singleton

chance = lambda x: not randint(0, x)


class Spring(sprite.Sprite):

    def __init__(self, parent: sprite.Sprite, images: pygame.image,
                 force=config.PLAYER_SPRING_JUMPFORCE):
        super().__init__()
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.get_inital_pos()
        self.parent = parent
        self.force = force

    def get_inital_pos(self):
        x = randint(self.parent.rect.left + 20, self.parent.rect.right - 20)
        y = self.parent.rect.y - config.SPRING_SIZE[1]
        return x, y

    def onCollide(self):
        self.image = self.images[1]


class Trampolin(sprite.Sprite):
    """
    A class to represent a bonus
    Inherits the Sprite class.
    """

    WIDTH = 45
    HEIGHT = 20

    def __init__(self, parent: sprite.Sprite, images: pygame.image,
                 force=config.PLAYER_TRAMP_JUMPFORCE):
        super().__init__()
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.get_inital_pos()
        self.parent = parent
        self.force = force

    def get_inital_pos(self):
        x = self.parent.rect.centerx - Trampolin.WIDTH // 2
        y = self.parent.rect.y - Trampolin.HEIGHT
        return x, y

    def onCollide(self):
        pass


class Platform(sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y,
                 initial_spring=False, initial_tramp=False, breakable=False, moveable=False):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.__level = Level.instance
        self.breakable = breakable
        self.moveable = moveable
        self.__bonus = None
        self.__type = None
        self.x_speed = 0

    @property
    def bonus(self):
        return self.__bonus

    def move(self):
        min_x = randint(0, config.XWIN - 50)
        max_x = randint(min_x, config.XWIN)
        speed = 3
        if self.rect.right > max_x:
            speed *= -1
        if self.rect.left < min_x:
            speed *= -1
        self.rect.center += speed

    def add_bonus(self, bonus_type: type) -> None:
        assert issubclass(bonus_type, (Spring, Trampolin)), "Not a valid bonus type !"
        if not self.__bonus and not self.breakable:
            self.__bonus = bonus_type(self)

    def remove_bonus(self) -> None:
        self.__bonus = None

    def onCollide(self) -> None:
        if self.breakable:
            self.__level.remove_platform(self)

    def draw(self, surface: Surface) -> None:
        if self.__bonus:
            self.__bonus.draw(surface)
        if self.camera_rect.y + self.rect.height > config.YWIN:
            self.__level.remove_platform(self)

    def update(self):
        if self.moveable:
            self.move()


class Level(Singleton):
    """
    A class to represent the level.

    used to manage updates/generation of platforms.
    Can be access via Singleton: Level.instance.
    (Check Singleton design pattern for more info)
    """

    # constructor called on new instance: Level()
    def __init__(self):
        self.platform_size = config.PLATFORM_SIZE
        self.max_platforms = config.MAX_PLATFORM_NUMBER
        self.distance_min = min(config.PLATFORM_DISTANCE_GAP)
        self.distance_max = max(config.PLATFORM_DISTANCE_GAP)

        self.spring_platform_chance = config.SPRING_SPAWN_CHANCE
        self.tramp_platform_chance = config.TRAMP_SPAWN_CHANCE
        self.breakable_platform_chance = config.BREAKABLE_PLATFORM_CHANCE

        self.__platforms = []
        self.__to_remove = []

        self.__base_platform = Platform(
            config.HALF_XWIN - self.platform_size[0] // 2,  # X POS
            config.HALF_YWIN + config.YWIN / 3,  # Y POS
            *self.platform_size)  # SIZE

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
                randint(0, config.XWIN - self.platform_size[0]),  # X POS
                self.__platforms[-1].rect.y - offset,  # Y POS
                *self.platform_size,  # SIZE
                initial_spring=chance(self.spring_platform_chance),
                initial_tramp=chance(self.tramp_platform_chance),  # HAS A Bonus
                breakable=chance(self.breakable_platform_chance)))  # IS BREAKABLE
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
        for platform in self.__to_remove:
            if platform in self.__platforms:
                self.__platforms.remove(platform)
        self.__to_remove = []
        asyncio.run(self._generation())

    def draw(self, surface: Surface) -> None:
        """ Called each frame in main loop, draws each platform
        :param surface pygame.Surface: the surface to draw on.
        """
        for platform in self.__platforms:
            platform.draw(surface)
