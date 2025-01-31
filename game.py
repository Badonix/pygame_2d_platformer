import pygame
import sys

from scripts.utils import load_image, Animation, load_images
from scripts.entities import Player

from scripts.tilemap import Tilemap

from scripts.clouds import Clouds


class Game:
    def __init__(self):
        pygame.init()

        self.SCALE = 2.0
        pygame.display.set_caption("FUCKING GAME")
        self.screen = pygame.display.set_mode((640, 480))

        # Display is half of screen, it is an empty image all black
        # I just render on this and then scale up to screen
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        # [0] is going left, [1] is going right
        self.movement = [False, False]

        # Camera
        self.scroll = [0, 0]

        self.assets = {
            "player": load_image("entities/player.png"),
            "decor": load_images("tiles/decor"),
            "grass": load_images("tiles/grass"),
            "large_decor": load_images("tiles/large_decor"),
            "stone": load_images("tiles/stone"),
            "background": load_image("background.png"),
            "menu-background": load_image("menu-background.webp"),
            "clouds": load_images("clouds"),
            "player/idle": Animation(load_images("entities/player/idle"), img_dur=6),
            "player/run": Animation(load_images("entities/player/run"), img_dur=4),
            "player/jump": Animation(load_images("entities/player/jump")),
            "player/slide": Animation(load_images("entities/player/slide")),
            "player/wall_slide": Animation(load_images("entities/player/wall_slide")),
        }
        self.clouds = Clouds(self.assets["clouds"], count=16)
        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load("map.json")

        self.player = Player(self, (50, 50), (8, 15))
        self.page = "menu"

    def run(self):
        while True:
            if self.page == "menu":
                self.display.blit(self.assets["menu-background"], (0, 0))
                start_rect = pygame.Rect(
                    (self.display.get_width() - 200) / 2, 10, 200, 50
                )
                pygame.draw.rect(self.display, (20, 20, 20), start_rect)
                self.screen.blit(
                    pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
                )
                mouse_pos = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if start_rect.collidepoint(
                                (mouse_pos[0] / self.SCALE, mouse_pos[1] / self.SCALE)
                            ):
                                self.page = "game"
                pygame.display.update()
            elif self.page == "game":
                render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
                self.display.blit(self.assets["background"], (0, 0))

                self.clouds.update()
                self.clouds.render(self.display, offset=render_scroll)

                # If we dont divide by 30 it wont be *smooth* animation
                self.tilemap.render(self.display, offset=render_scroll)
                self.scroll[0] += (
                    self.player.rect().centerx
                    - self.display.get_width() / 2
                    - self.scroll[0]
                ) / 20
                self.scroll[1] += (
                    self.player.rect().centery
                    - self.display.get_height() / 2
                    - self.scroll[1]
                ) / 20

                self.player.update(
                    self.tilemap, (self.movement[1] - self.movement[0], 0)
                )
                self.player.render(self.display, offset=render_scroll)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.movement[0] = True
                        if event.key == pygame.K_RIGHT:
                            self.movement[1] = True
                        if event.key == pygame.K_UP:
                            self.player.velocity[1] = -3
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                            self.movement[0] = False
                        if event.key == pygame.K_RIGHT:
                            self.movement[1] = False

                self.screen.blit(
                    pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
                )
                pygame.display.update()
                self.clock.tick(60)


Game().run()
