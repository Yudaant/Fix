import pygame.math as m
SCREEN_WIDTH = 610
SCREEN_HEIGHT = 670
TOP_BOTTOM = 50
MAZE_WIDTH, MAZE_HEIGHT = SCREEN_WIDTH - TOP_BOTTOM, SCREEN_HEIGHT - TOP_BOTTOM

FPS = 10
black = (0 , 0 , 0)
white = (255 , 255, 255)
red = (255 , 0 , 0)
blue = (0 , 0 , 255)
green = (0 , 255 , 0)

left = m.Vector2(-1 , 0)
right = m.Vector2(1 , 0)
up = m.Vector2(0 , -1)
down = m.Vector2(0 , 1)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
SILVER = (192, 192, 192)
GREY = (128, 128, 128)
MAROON = (128, 0, 0)
OLIVE = (128, 128, 0)
DARK_GREEN = (0, 128, 0)
PURPLE = (128, 0, 128)
TEAL = (0, 128, 128)
NAVY = (0, 0, 128)
ORANGE_RED = (255,69,0)
ORANGE = (255,165,0)
GOLD = (255,215,0)
GRAY_DARK = (104, 107, 106)
GRAY_LIGHT = (161, 166, 165)

default_font = "arial black"
default_size = 16

ROW = 31
COL = 28