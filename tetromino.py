import pygame as pg
from pygame.sprite import Sprite
from settings import *
import random

TETROMINOES = {
    'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
    'O': [(0, 0), (0, -1), (1, 0), (1, -1)],
    'J': [(0, 0), (-1, 0), (0, -1), (0, -2)],
    'L': [(0, 0), (1, 0), (0, -1), (0, -2)],
    'I': [(0, 0), (0, 1), (0, -1), (0, -2)],
    'S': [(0, 0), (-1, 0), (0, -1), (1, -1)],
    'Z': [(0, 0), (1, 0), (0, -1), (-1, -1)],
}

T_COLORS = {
    'T': pg.transform.scale(pg.image.load((f'images/sprites/purple.png')), (TILE_SIZE, TILE_SIZE)),
    'O': pg.transform.scale(pg.image.load((f'images/sprites/yellow.png')), (TILE_SIZE, TILE_SIZE)),
    'J': pg.transform.scale(pg.image.load((f'images/sprites/blue.png')), (TILE_SIZE, TILE_SIZE)),
    'L': pg.transform.scale(pg.image.load((f'images/sprites/orange.png')), (TILE_SIZE, TILE_SIZE)),
    'I': pg.transform.scale(pg.image.load((f'images/sprites/cyan.png')), (TILE_SIZE, TILE_SIZE)),
    'S': pg.transform.scale(pg.image.load((f'images/sprites/green.png')), (TILE_SIZE, TILE_SIZE)),
    'Z': pg.transform.scale(pg.image.load((f'images/sprites/red.png')), (TILE_SIZE, TILE_SIZE)),
}


class Block(Sprite):
    def __init__(self, tetromino, pos):
        self.tetromino = tetromino
        self.pos = vector(pos) + INIT_POS_OFFSET
        self.next_pos = vector(pos) + NEXT_POS_OFFSET
        self.alive = True

        super().__init__(tetromino.tetris.sprite_group)
        self.image = tetromino.image
        self.rect = self.image.get_rect()

        self.sfx_image = self.image.copy()
        self.sfx_image.set_alpha(110)
        self.sfx_speed = random.uniform(0.2, 0.6)
        self.sfx_cycles = random.randrange(6, 8)
        self.cycle_counter = 0

    def sfx_end_time(self):
        if self.tetromino.tetris.game.anim_trigger:
            self.cycle_counter += 1
            if self.cycle_counter > self.sfx_cycles:
                self.cycle_counter = 0
                return True
            
    def sfx_run(self):
        self.image = self.sfx_image
        self.pos.y -= self.sfx_speed
        self.image = pg.transform.rotate(self.image, pg.time.get_ticks() * self.sfx_speed)
    
    def is_alive(self):
        if not self.alive:
            if not self.sfx_end_time():
                self.sfx_run()
            else:
                self.kill()

    def rotate(self, pivot_pos):
        translated = self.pos - pivot_pos
        rotated = translated.rotate(90)
        return rotated + pivot_pos
    
    def set_rect_pos(self):
        pos = [self.next_pos, self.pos][self.tetromino.current]
        self.rect.topleft = pos * TILE_SIZE

    def update(self):
        self.is_alive()
        self.set_rect_pos()

    def is_collide(self, pos):
        x, y = int(pos.x), int(pos.y)
        if 0 <= x < FIELD_W and y < FIELD_H and (y < 0 or not self.tetromino.tetris.field_array[y][x]):
            return False
        return True

class Tetromino:
    def __init__(self, tetris, current=True):
        self.tetris = tetris
        self.shape = random.choice(list(TETROMINOES.keys()))
        self.image = T_COLORS.get(self.shape)
        self.blocks = [Block(self, pos) for pos in TETROMINOES[self.shape]]
        self.landing = False
        self.current = current
    
    def rotate(self):
        pivot_pos = self.blocks[0].pos
        new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

        if not self.is_collide(new_block_positions):
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]

    def is_collide(self, block_positions):
        return any(map(Block.is_collide, self.blocks, block_positions))
    
    def move(self, direction):
        move_direction = MOVE_DIRECTIONS[direction]
        new_block_positions = [block.pos + move_direction for block in self.blocks]
        is_collide = self.is_collide(new_block_positions)

        if not is_collide:
            for block in self.blocks:
                block.pos += move_direction
        elif direction == 'down':
            self.landing = True

    def update(self):
        self.move(direction='down')

if __name__ == '__main__':
  print("\nERROR: tetromino.py is the wrong file! Run play from game.py\n")