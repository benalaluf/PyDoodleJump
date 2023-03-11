import pygame, sys
from pygame.font import SysFont
import settings as config

from button import Button
from newGame.game import Game

pygame.init()

SCREEN = pygame.display.set_mode((640, 1024))
pygame.display.set_caption("Menu")

BG = pygame.image.load("images/r/background.png")

alive = True

class Menus:
    def __init__(self):
        self.game = Game()

    def get_font(self,size):  # Returns Press-Start-2P in the desired size
        return SysFont("arial-bold", size)


    def play(self):
        self.game.reset()
        self.game.run()



    def options(self):
        while True:
            global  BG
            SCREEN.blit(BG, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(60).render("Themes", True, "Blue")
            MENU_RECT = MENU_TEXT.get_rect(center=(config.HALF_XWIN, 100))

            PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(config.HALF_XWIN, 250),
                                 text_input="regular", font=self.get_font(50), base_color="black", hovering_color="white")
            OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(config.HALF_XWIN, 400),
                                    text_input="ben", font=self.get_font(50), base_color="black", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(config.HALF_XWIN, 550),
                                 text_input="passhover", font=self.get_font(50), base_color="black", hovering_color="White")
            BACK_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(config.HALF_XWIN, 700),
                                 text_input="back", font=self.get_font(50), base_color="black", hovering_color="White")

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
                        BG = pygame.image.load("images/b/background.png")
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        config.setTheme('s')
                    if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.main_menu()
            config.loadTheme()
            pygame.display.update()


    def playagain(self):
        while True:
            SCREEN.blit(BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(config.HALF_XWIN, 250),
                                 text_input="play again", font=self.get_font(50), base_color="black", hovering_color="white")
            OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(config.HALF_XWIN, 400),
                                    text_input="themes", font=self.get_font(50), base_color="black", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(config.HALF_XWIN, 550),
                                 text_input="passhover", font=self.get_font(50), base_color="black", hovering_color="White")
            BACK_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(config.HALF_XWIN, 700),
                                 text_input="back", font=self.get_font(50), base_color="black", hovering_color="White")

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, BACK_BUTTON]:
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
                    if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        global  alive
                        alive = True
                        self.main_menu()

            pygame.display.update()


    def main_menu(self):
        while alive:
            SCREEN.blit(BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(60).render("Doodle Jump", True, "Blue")
            MENU_RECT = MENU_TEXT.get_rect(center=(config.HALF_XWIN, 100))

            PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(config.HALF_XWIN, 250),
                                 text_input="PLAY", font=self.get_font(50), base_color="black", hovering_color="white")
            OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(config.HALF_XWIN, 400),
                                    text_input="Themes", font=self.get_font(50), base_color="black", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(config.HALF_XWIN, 550),
                                 text_input="QUIT", font=self.get_font(50), base_color="black", hovering_color="White")

            SCREEN.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
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

            pygame.display.update()



