import pygame
import settings as config


class Menu():
    def __init__(self):
        self.__alive = True
        self.window = pygame.display.set_mode(config.DISPLAY, config.FLAGS)
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -100

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(config.MENU_FONT, size)
        text_surface = font.render(text, True, config.MENU_TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.window.blit(text_surface, text_rect)

    def draw_cursor(self):
        self.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.window.blit(self.window, (0, 0))
        pygame.display.update()


class MainMenu(Menu):
    def __init__(self):
        Menu.__init__(self)
        self.state = 'Start'
        self.startx, self.starty = config.HALF_XWIN, config.HALF_YWIN + 30
        self.optionsx, self.optionsy = config.HALF_XWIN, config.HALF_YWIN + 50
        self.creditsx, self.creditsy = config.HALF_XWIN, config.HALF_YWIN + 70
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
       self.run_display = True
       while self.run_display:
           self.window.fill(config.BLACK)