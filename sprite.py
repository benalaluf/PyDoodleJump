import pygame.image
from pygame.rect import Rect
from pygame.surface import Surface

from camera import Camera


class Sprite:

    # default constructor (must be called if overrided by inheritance)
    def __init__(self, x: int, y: int, w: int, h: int, image: str):
        self._w = w
        self._h = h
        self._image = pygame.image.load(image)
        self._image = pygame.transform.scale(self._image, (w, h))
        self.rect = Rect(x, y, w, h)
        self.camera_rect = self.rect.copy()

    # Public getters for _image & __color so they remain private
    @property
    def image(self) -> Surface:
        return self._image

    def set_image(self, image, w =None,  h=None):
        if w == None:
            w = self._h
        if h == None:
            h = self._h
        self._image = pygame.image.load(image)
        self._image = pygame.transform.scale(self._image, (w, h))

    @property
    def color(self) -> tuple:
        return self.__color

    @color.setter
    def color(self, new: tuple) -> None:
        " Called when Sprite.__setattr__('color',x)."
        assert isinstance(new, tuple) and len(new) == 3, "Value is not a color"
        self.__color = new
        # update image surface
        self._image.fill(self.color)

    def getRect(self):
        return self.rect

    def draw(self, surface: Surface) -> None:
        """ Render method,Should be called every frame after update.
        :param surface pygame.Surface: the surface to draw on.
        """
        # If camera instancied: calculate render positon
        if Camera.instance:
            self.camera_rect = Camera.instance.apply(self)
            surface.blit(self._image, self.camera_rect)
        else:
            surface.blit(self._image, self.rect)
