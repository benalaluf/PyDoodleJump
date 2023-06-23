import pygame

# General SetUp
from camera import Camera
from level import Level
from player import Player
import settings as config
from singleton import Singleton

class Game(Singleton):
    def __init__(self):
        self.__alive = True
        # Game Screen
        screen_width = 640
        screen_height = 1024
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

        # Camera
        self.camera = Camera()

        # Player
        self.player = Player()
        self.dead_sound = pygame.mixer.Sound('sounds/pada.mp3')
        self.dead_flag = False


        # Platfor
        self.level = Level()
        # User Interface
        self.score = 0
        self.score_txt = config.SMALL_FONT.render("0 m", 1, config.GRAY)
        self.score_pos = pygame.math.Vector2(10, 10)

        self.gameover_txt = config.LARGE_FONT.render("Game Over", 1, config.GRAY)
        self.gobacktomenu_txt = config.SMALL_FONT.render("Press Enter To Menu", 1, config.GRAY)
        self.gameover_rect = self.gameover_txt.get_rect(
            center=(config.HALF_XWIN, config.HALF_YWIN))
        self.gobacktomenu_rect = self.gameover_txt.get_rect()
        self.gobacktomenu_rect.center = [config.HALF_XWIN+5, config.HALF_YWIN+70]

    def choose_theme(self,theme):
        self.theme = theme

    def close(self):
        self.__alive = False

    def reset(self):
        self.__alive = True
        self.camera.reset()
        self.level.reset()
        self.player.reset()
        self.dead_flag = False


    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.close()
                if event.key == pygame.K_RETURN and self.player.dead:
                    self.close()
            self.player.handle_event(event)
        if self.player.dead and not self.dead_flag:
            self.dead_sound.play()
            self.dead_flag = True

    def render_loop(self):
        self.screen.blit(config.BACKGROUND, (0, 0))
        self.level.draw(self.screen)
        self.player.draw(self.screen)
        # for b in self.player.bullets:
        #     pygame.draw.rect(self.screen, pygame.Color("red"), b.rect, 2)
        if self.player.dead:
            self.screen.blit(self.gameover_txt, self.gameover_rect)  # gameover txt
            self.screen.blit(self.gobacktomenu_txt, self.gobacktomenu_rect)  # gameover txt


        self.screen.blit(self.score_txt, self.score_pos)  # score txt
        pygame.display.flip()
        self.clock.tick(60)

    def update_loop(self):
        self.level.update()
        self.player.update()
        if not self.player.dead:
            self.camera.update(self.player.rect)
            # calculate score and update UI txt
            self.score = -self.camera.state.y // 50
            self.score_txt = config.SMALL_FONT.render(
                str(self.score) + " m", 1, config.GRAY)
        config.loadTheme()

    def run(self):
        # ============= MAIN GAME LOOP =============
        while self.__alive:
            self.event_loop()
            self.update_loop()
            self.render_loop()
