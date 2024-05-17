import pygame as pg


vector = pg.math.Vector2

FPS = 60
FIELD_COLOR = (48, 39, 32)
BG_COLOR = (0, 0, 0)

LAUNCH_BG = (255, 255, 255)


ANIM_TIME_INTERVAL = 300
FAST_ANIM_TIME_INTERVAL = 15

TILE_SIZE = 50
FIELD_SIZE = FIELD_W, FIELD_H = 10, 20
FIELD_RES = FIELD_W * TILE_SIZE, FIELD_H * TILE_SIZE

FIELD_SCALE_W, FIELD_SCALE_H = 1.7, 1.0
WIN_RES = WIN_W, WIN_H = FIELD_RES[0] * FIELD_SCALE_W, FIELD_RES[1] * FIELD_SCALE_H

INIT_POS_OFFSET = vector(FIELD_W // 2 - 1, 0)
NEXT_POS_OFFSET = vector(FIELD_W * 1.3, FIELD_H * 0.37)
MOVE_DIRECTIONS = {'left': vector(-1, 0), 'right': vector(1, 0), 'down': vector(0, 1)}

if __name__ == '__main__':
  print("\nERROR: settings.py is the wrong file! Run play from game.py\n")