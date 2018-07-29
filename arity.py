import pygame
from pygame.locals import *

import time, math, sys, json

from game import game as game


pygame.mixer.pre_init(44100, -16, 2, 128)

pygame.init()
pygame.font.init()

pygame.mixer.init(44100)

config = json.load(open('config.json', 'r'))

g = game.Game(config)

g.run()


