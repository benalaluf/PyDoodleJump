# button class
import sys

import pygame
import settings as config
from newGame.level import Platform
from newGame.singleton import Singleton


class MainMenu(Singleton):
    def __init__(self):
        self._allve = True
        self.clock = pygame.time.Clock()
        screen_width = 640
        screen_height = 1024
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.background = pygame.image.load('images/r/background.png')
        self.MENU_TEXT = self.get_font(30).render("Doodle Jump", True, pygame.Color(0, 80, 200))
        self.MENU_RECT = self.MENU_TEXT.get_rect(center=(config.HALF_XWIN, 100))
        self.MENU_MOUSE_POS = 0, 0
        self.PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(300, 250),
                                  text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4",
                                  hovering_color="White")
        self.OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(300, 400),
                                     text_input="THEMES", font=self.get_font(75), base_color="#d7fcd4",
                                     hovering_color="White")
        self.QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(300, 550),
                                  text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4",
                                  hovering_color="White")
        # self.platform_pos = [100, 700]
        # self.player_pos = [self.platform_pos[0] + 10, self.platform_pos[1] - 50]
        # self.player = self.game.player()
        # self.player.rect.topleft = self.player_pos
        # self.platform = Platform(self.platform_pos[0], self.platform_pos[1])

    def get_font(self, size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("assets/font.ttf", size)

    def render_loop(self):
        self.screen.blit(self.background, (0, 0))

        self.screen.blit(self.MENU_TEXT, self.MENU_RECT)
        for button in [self.PLAY_BUTTON, self.OPTIONS_BUTTON, self.QUIT_BUTTON]:
            button.changeColor(self.MENU_MOUSE_POS)
            button.update(self.screen)
        #
        # self.player.draw(self.screen)
        # self.platform.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)

    def update_loop(self):
        self.MENU_MOUSE_POS = pygame.mouse.get_pos()
        # self.player.update()
        # self.platform.update()
        # self.player.update_collisoins(self.platform)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.PLAY_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    self._allve = False
                if self.OPTIONS_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    config.instant.setTheme('b')
                if self.QUIT_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

    def run(self):
        # ============= MAIN GAME LOOP =============
        while self._allve:
            self.event_loop()
            self.update_loop()
            self.render_loop()

class ThemesMenu(Singleton):
    def __init__(self):
        self._allve = True
        self.clock = pygame.time.Clock()
        screen_width = 640
        screen_height = 1024
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.background = pygame.image.load('images/r/background.png')
        self.MENU_TEXT = self.get_font(30).render("Themes", True, pygame.Color(0, 80, 200))
        self.MENU_RECT = self.MENU_TEXT.get_rect(center=(config.HALF_XWIN, 100))
        self.MENU_MOUSE_POS = 0, 0
        self.PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(300, 250),
                                  text_input="regular", font=self.get_font(75), base_color="#d7fcd4",
                                  hovering_color="White")
        self.OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(300, 400),
                                     text_input="passhover", font=self.get_font(75), base_color="#d7fcd4",
                                     hovering_color="White")
        self.QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(300, 550),
                                  text_input="ben", font=self.get_font(75), base_color="#d7fcd4",
                                  hovering_color="White")
        # self.platform_pos = [100, 700]
        # self.player_pos = [self.platform_pos[0] + 10, self.platform_pos[1] - 50]
        # self.player = self.game.player()
        # self.player.rect.topleft = self.player_pos
        # self.platform = Platform(self.platform_pos[0], self.platform_pos[1])

    def get_font(self, size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("assets/font.ttf", size)

    def render_loop(self):
        self.screen.blit(self.background, (0, 0))

        self.screen.blit(self.MENU_TEXT, self.MENU_RECT)
        for button in [self.PLAY_BUTTON, self.OPTIONS_BUTTON, self.QUIT_BUTTON]:
            button.changeColor(self.MENU_MOUSE_POS)
            button.update(self.screen)
        #
        # self.player.draw(self.screen)
        # self.platform.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)

    def update_loop(self):
        self.MENU_MOUSE_POS = pygame.mouse.get_pos()
        # self.player.update()
        # self.platform.update()
        # self.player.update_collisoins(self.platform)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.PLAY_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    self._allve = False
                if self.OPTIONS_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                   config.setTheme('b')
                if self.QUIT_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

    def run(self):
        # ============= MAIN GAME LOOP =============
        while self._allve:
            self.event_loop()
            self.update_loop()
            self.render_loop()

class PLAY_AGAIN():
    def __init__(self, game):
        self.__alive = True
        self.clock = pygame.time.Clock()
        screen_width = 640
        screen_height = 1024
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.background = pygame.image.load('images/b/background.png')
        self.MENU_TEXT = self.get_font(10).render("Doodle Jump", True, pygame.Color(0, 80, 200))
        self.MENU_RECT = self.MENU_TEXT.get_rect(center=(config.HALF_XWIN, 100))
        self.MENU_MOUSE_POS = 0, 0
        self.PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(300, 250),
                                  text_input="PLAY again", font=self.get_font(75), base_color="#d7fcd4",
                                  hovering_color="White")
        self.game = game

    def get_font(self, size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("assets/font.ttf", size)

    def render_loop(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.MENU_TEXT, self.MENU_RECT)
        for button in [self.PLAY_BUTTON]:
            button.changeColor(self.MENU_MOUSE_POS)
            button.update(self.screen)
        pygame.display.flip()
        self.clock.tick(60)

    def update_loop(self):
        self.MENU_MOUSE_POS = pygame.mouse.get_pos()

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.PLAY_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    self.__alive = False
                    self.game.reset()

        pygame.display.update()

    def run(self):
        # ============= MAIN GAME LOOP =============
        self.__alive = True
        while self.__alive:
            self.event_loop()
            self.update_loop()
            self.render_loop()


class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
