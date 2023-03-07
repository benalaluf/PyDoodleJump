from random import randint
from pygame import Surface
import asyncio

from singleton import Singleton
from sprite import Sprite
import settings as config

# return True with a chance of: P(X=True)=1/x
chance = lambda x: not randint(0, x)


class Spring(Sprite):
    """
    A class to represent a bonus
    Inherits the Sprite class.
    """

    WIDTH = 30
    HEIGHT = 25

    def __init__(self, parent: Sprite, image=config.PLATFORM_SPRING_IMAGE,
                 force=config.PLAYER_SPRING_JUMPFORCE):
        self.parent = parent
        super().__init__(self._get_inital_pos()[0], self._get_inital_pos()[1],
                         Spring.WIDTH, Spring.HEIGHT, image)
        self.force = force

    def _get_inital_pos(self):
        x = self.parent.rect.centerx - Spring.WIDTH // 2
        y = self.parent.rect.y - Spring.HEIGHT
        return x, y

    def onCollide(self):
        self.set_image(config.PLATFORM_SPRING_OPEN_IMAGE,h=60)


class Trampolin(Sprite):
    """
    A class to represent a bonus
    Inherits the Sprite class.
    """

    WIDTH = 40
    HEIGHT = 15

    def __init__(self, parent: Sprite, image=config.PLATFORM_TRAMP_IMAGE,
                 force=config.PLAYER_TRAMP_JUMPFORCE):
        self.parent = parent
        super().__init__(self._get_inital_pos()[0],self._get_inital_pos()[1],
                         Trampolin.WIDTH, Trampolin.HEIGHT, image)
        self.force = force

    def _get_inital_pos(self):
        x = self.parent.rect.centerx - Trampolin.WIDTH // 2
        y = self.parent.rect.y - Trampolin.HEIGHT
        return x, y

    def onCollide(self):
        pass


class Platform(Sprite):

    # (Overriding inherited constructor: Sprite.__init__)
    def __init__(self, x: int, y: int, width: int, height: int,
                 initial_spring=False, initial_tramp =False, breakable=False):
        image = config.PLATFORM_BASE_IMAGE
        if breakable: image = config.PLATFORM_BREAKABLE_IMAGE
        super().__init__(x, y, width, height, image)

        self.rect = self.getRect().inflate(0,-30)
        self.breakable = breakable
        self.__level = Level.instance
        self.__bonus = None
        self.__type = None
        if initial_spring:
            self.add_bonus(Spring)
        if initial_tramp:
            self.add_bonus(Trampolin)

    # Public getter for __bonus so it remains private
    @property
    def bonus(self):
        return self.__bonus

    @property
    def type(self):
        return self.__type

    def add_bonus(self, bonus_type: type) -> None:
        """ Safely adds a bonus to the platform.
        :param bonus_type type: the type of bonus to add.
        """
        assert issubclass(bonus_type, (Spring, Trampolin)), "Not a valid bonus type !"
        if not self.__bonus and not self.breakable:
            self.__bonus = bonus_type(self)
            self.__type = type(bonus_type(self))

    def remove_bonus(self) -> None:
        " Safely removes platform's bonus."
        self.__bonus = None

    def onCollide(self) -> None:
        " Called in update if collision with player (safe to overrided)."
        if self.breakable:
            self.__level.remove_platform(self)

    # ( Overriding inheritance: Sprite.draw() )
    def draw(self, surface: Surface) -> None:
        """ Like Sprite.draw().
        Also draws the platform's bonus if it has one.
        :param surface pygame.Surface: the surface to draw on.
        """
        # check if out of screen: should be deleted
        super().draw(surface)
        if self.__bonus:
            self.__bonus.draw(surface)
        if self.camera_rect.y + self.rect.height > config.YWIN:
            self.__level.remove_platform(self)


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
                initial_tramp=chance(self.tramp_platform_chance),# HAS A Bonus
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
