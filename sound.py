import pygame as pg
import time


class Sound:
    def __init__(self, bg_music):
        pg.mixer.init()
        pg.mixer.music.load(bg_music)
        pg.mixer.music.set_volume(0.2)    

    def play_bg(self, bg_music):
        self.stop_bg()
        pg.mixer.music.load(bg_music)
        pg.mixer.music.play(-1, 0.0)

    def stop_bg(self):
        pg.mixer.music.stop()

    def pause_bg(self): 
        pg.mixer.music.pause()

    def unpause_bg(self):
        pg.mixer.music.unpause()     

    def game_over(self): 
        self.stop_bg() 
        self.play_bg('sounds/game_over.wav')
        time.sleep(2.8)
        self.stop_bg()


if __name__ == '__main__':
  print("\nERROR: sound.py is the wrong file! Run play from game.py\n")