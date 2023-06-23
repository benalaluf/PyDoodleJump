import pygame, sys
from pygame.font import SysFont
import settings as config
from button import Button
from game import Game
from level import Platform
from player import Player

pygame.init()

SCREEN = pygame.display.set_mode((640, 1024))
pygame.display.set_caption("Menu")
clock = pygame.time.Clock()

BG = pygame.image.load("images/r/background.png")
how = pygame.transform.scale(pygame.image.load("images/howtoplay.png"), (640, 464))

alive = True


class Menus:
    def __init__(self):
        self.game = Game()
        self.player = Player.instance
        self.player.rect.topleft = [100, 500]
        self.platform = Platform(100, 600)

    def get_font(self, size):  # Returns Press-Start-2P in the desired size
        return SysFont("Chalkboard SE", size)

    def play(self):
        self.game.reset()
        self.game.run()

    def options(self):
        while True:
            global BG
            SCREEN.blit(BG, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(80).render("Themes", True, "black")
            MENU_RECT = MENU_TEXT.get_rect(center=(config.HALF_XWIN, 100))

            PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(config.HALF_XWIN, 250),
                                 text_input="Regular", font=self.get_font(50), base_color="black",
                                 hovering_color="white")
            OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(config.HALF_XWIN, 400),
                                    text_input="Ben", font=self.get_font(50), base_color="black",
                                    hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(config.HALF_XWIN, 550),
                                 text_input="Passover", font=self.get_font(50), base_color="black",
                                 hovering_color="White")
            BACK_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(config.HALF_XWIN, 700),
                                 text_input="Back", font=self.get_font(50), base_color="black", hovering_color="White")

            SCREEN.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, BACK_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        config.setTheme('r')
                        BG = pygame.image.load("images/r/background.png")
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        config.setTheme('b')
                        BG = pygame.transform.scale(pygame.image.load(f'images/b/background.png'),
                                                    (config.XWIN, config.YWIN))
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        config.setTheme('s')
                        BG = pygame.image.load("images/s/background.png")
                    if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.main_menu()

            config.loadTheme()
            pygame.display.update()

    def howto(self):
        while True:
            SCREEN.blit(BG, (0, 0))
            SCREEN.blit(how, (0, 50))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            BACK_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(config.HALF_XWIN, 700),
                                 text_input="back", font=self.get_font(50), base_color="black", hovering_color="White")

            for button in [BACK_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.main_menu()

            pygame.display.update()

    def main_menu(self):
        self.player = Player.instance
        self.player.dead = False
        self.player.rect.topleft = [70, 500]
        self.platform = Platform(70, 600)
        while alive:
            SCREEN.blit(BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(80).render("Doodle Jump", True, "Black")
            MENU_RECT = MENU_TEXT.get_rect(center=(config.HALF_XWIN, 100))

            PLAY_BUTTON = Button(image=None, pos=(250, 250),
                                 text_input="PLAY", font=self.get_font(50), base_color="black", hovering_color="gray")
            OPTIONS_BUTTON = Button(image=None, pos=(350, 400),
                                    text_input="THEME", font=self.get_font(50), base_color="black",
                                    hovering_color="gray")
            QUIT_BUTTON = Button(image=None, pos=(450, 550),
                                 text_input="QUIT", font=self.get_font(50), base_color="black", hovering_color="gray")
            HOW_BUTTON = Button(image=None, pos=(320, 900),
                                text_input="HOW TO PLAY", font=self.get_font(50), base_color="black",
                                hovering_color="gray")

            SCREEN.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, HOW_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.play()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()
                    if HOW_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.howto()

            self.player.update()
            self.player.draw(SCREEN)
            self.player.update_collisoins(self.platform)
            self.platform.draw(SCREEN)

            clock.tick(60)
            pygame.display.update()
