import pygame.image
from pygame.rect import Rect
from pygame.surface import Surface

from camera import Camera


class Sprite:

    # default constructor (must be called if overrided by inheritance)
    def __init__(self, x: int, y: int, w: int, h: int, image: pygame.image):
        self._w = w
        self._h = h
        self._image = image
        self.rect = Rect(x, y, w, h)
        self.camera_rect = self.rect.copy()

    # Public getters for _image & __color so they remain private
    @property
    def image(self) -> Surface:
        return self._image

    def set_image(self, image, w=None, h=None):
        self._image = image
        if w is not None and h is not None:
            self._image = pygame.transform.scale(self._image, (w, h))
        if w is not None:
            self._image = pygame.transform.scale(self._image, (w, self._h))
        if h is not None:
            self._image = pygame.transform.scale(self._image, (self._w, h))

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

    def collided(self, other_rect):
        # Return True if self collided with other_rect
        return self.rect.colliderect(other_rect)
