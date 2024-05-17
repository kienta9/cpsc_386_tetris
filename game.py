import pygame as pg
import sys
from settings import *
from tetris import Tetris, Text
from sound import Sound
from button import Button

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(WIN_RES)
        pg.display.set_caption('Tetris')
        self.clock = pg.time.Clock()
        self.set_timer()
        self.sound = Sound("sounds/theme.wav")
        self.tetris = Tetris(self)
        self.text = Text(self)
        self.launch_screen()

    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.anim_trigger = False
        self.fast_anim_trigger = False
        pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_event, FAST_ANIM_TIME_INTERVAL)

    def update(self):
        self.clock.tick(FPS)
        self.tetris.update()

    def draw(self):
        self.screen.fill(color=BG_COLOR)
        self.screen.fill(color=FIELD_COLOR, rect =(0, 0, *FIELD_RES))
        self.tetris.draw()
        self.text.draw()
        pg.display.flip()

    def check_events(self):
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.tetris.control(key = event.key)
            elif event.type == self.user_event:
                self.anim_trigger = True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True

    def launch_screen(self):
        launch = True
        play_button = Button(self.screen, (WIN_RES[0] - 300) // 2 , (WIN_RES[1] - 50) // 2 + 120, 300, 50, "Play")

        image = pg.transform.scale(pg.image.load(f'images/launch.jpg'), (WIN_RES[0], WIN_RES[1]))
        image_rect = image.get_rect()

        while launch:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if play_button.is_clicked():
                        launch = False
                        pg.mouse.set_visible(False)
                        self.sound.play_bg("sounds/theme.wav")
                        
            play_button.update()
            
            self.screen.fill(color=BG_COLOR)

            self.screen.blit(image, image_rect)

            play_button.draw()

            pg.display.flip()

    def play(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    g = Game()
    g.play()
