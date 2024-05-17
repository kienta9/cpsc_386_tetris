import pygame as pg
from settings import *
from tetromino import Tetromino
import pygame.freetype as ft
from sound import Sound


class Text:
    def __init__(self, game):
        self.game = game
        self.font = ft.Font('font/font.ttf')

    def draw(self):
        self.font.render_to(self.game.screen, (WIN_W * 0.61, WIN_H * 0.02),
                            text='TETRIS', fgcolor='#F5F5F5',
                            size=TILE_SIZE * 1.65)
        self.font.render_to(self.game.screen, (WIN_W * 0.725, WIN_H * 0.19),
                            text='Next', fgcolor='#A52A2A',
                            size=TILE_SIZE)
        self.font.render_to(self.game.screen, (WIN_W * 0.6, WIN_H * 0.6),
                            text='High:', fgcolor='#FF0000',
                            size=TILE_SIZE)
        self.font.render_to(self.game.screen, (WIN_W * 0.61, WIN_H * 0.7),
                            text=f'{self.game.tetris.high_score}', fgcolor='#FFD700',
                            size=TILE_SIZE * 1.4)
        self.font.render_to(self.game.screen, (WIN_W * 0.6, WIN_H * 0.8),
                            text='Score:', fgcolor='#00FF00',
                            size=TILE_SIZE)
        self.font.render_to(self.game.screen, (WIN_W * 0.61, WIN_H * 0.9),
                            text=f'{self.game.tetris.score}', fgcolor='#F8F8F8',
                            size=TILE_SIZE * 1.4)
        


class Tetris:
    def __init__(self, game):
        self.game = game
        self.sprite_group = pg.sprite.Group()
        self.field_array = self.get_field_array()
        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current=False)
        self.speed_up = False
        self.sound = game.sound

        self.score = 0
        self.high_score = self.load_high_score()
        self.full_lines = 0
        self.points_per_lines = {0: 0, 1: 100, 2: 300, 3: 600, 4: 1000}

    def get_score(self):
        self.score += self.points_per_lines[self.full_lines]
        self.check_high_score()
        self.full_lines = 0

    def load_high_score(self):
        try:
            with open('highscore.txt', 'r') as file:
                return int(file.read())
        except FileNotFoundError:
            return 0
        
    def save_high_score(self, score):
        with open('highscore.txt', 'w') as file:
            file.write(str(score))

    def check_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score(self.score)

    def check_full_lines(self):
        row = FIELD_H - 1
        for y in range(FIELD_H - 1, -1, -1):
            for x in range(FIELD_W):
                self.field_array[row][x] = self.field_array[y][x]

                if self.field_array[y][x]:
                    self.field_array[row][x].pos = vector(x, y)

            if sum(map(bool, self.field_array[y])) < FIELD_W:
                row -= 1
            else:
                for x in range(FIELD_W):
                    self.field_array[row][x].alive = False
                    self.field_array[row][x] = 0
                
                self.full_lines += 1

    def put_tetromino_blocks_in_array(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block

    def get_field_array(self):
        return [[0 for x in range(FIELD_W)] for y in range(FIELD_H)]
    
    def is_game_over(self):
        if self.tetromino.blocks[0].pos.y == INIT_POS_OFFSET[1]:
            return True
    
    def check_tetromino_landing(self):
        if self.tetromino.landing:
            if self.is_game_over():
                self.sound.game_over()
                self.__init__(self.game)
                pg.mouse.set_visible(True)
                self.game.launch_screen()
            else:
                self.speed_up= False
                self.put_tetromino_blocks_in_array()
                self.next_tetromino.current = True
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino(self, current=False)

    def control(self, key):
        if key == pg.K_LEFT:
            self.tetromino.move(direction='left')
        elif key == pg.K_RIGHT:
            self.tetromino.move(direction='right')
        elif key == pg.K_UP:
            self.tetromino.rotate()
        elif key == pg.K_DOWN:
            self.speed_up = True

    def draw_grid(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.game.screen, 'black', (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
    
    def update(self):
        trigger = [self.game.anim_trigger, self.game.fast_anim_trigger][self.speed_up]
        if trigger:
            self.check_full_lines()
            self.tetromino.update()
            self.check_tetromino_landing()
            self.get_score()
        self.sprite_group.update()

    def draw(self):
        self.draw_grid()
        self.sprite_group.draw(self.game.screen)

if __name__ == '__main__':
  print("\nERROR: tetris.py is the wrong file! Run play from game.py\n")