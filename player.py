import pygame
from pygame.locals import *


class Player():

    def __init__(self, game, config):
        self.g = game
        self.pos = config.get('start_pos', [400,300])
        self.vel = [0,0]
        self.jump = 0
        self.jump_tol = 0
        self.jump_count = 0

    def event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_z:
                self.g.map.do_jump(self)

    def can_jump(self):
        return abs(self.vel[1]) <= self.jump_tol
        return self.jump == 0

    def tick(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            if self.jump > 0:
                self.vel[0] -= .5
            else:
                self.vel[0] = -4
        elif keys[K_RIGHT]:
            if self.jump > 0:
                self.vel[0] += .5
            else:
                self.vel[0] = 4

        if self.vel[0] > 4: self.vel[0] = 4
        if self.vel[0] < -4: self.vel[0] = -4

        self.g.map.do_player(self)

    def render(self):
        screen = self.g.get_screen(0)
        ipos = list(map(int, self.pos))

        rad = min(abs(self.vel[1]), 10)
        a = int(255*(rad/10.))

        pygame.draw.circle(screen, (a,a,a), ipos, int(rad))

        if self.can_jump():
            pygame.draw.circle(screen, (255,255,255), ipos, 5)

        screen.set_at(ipos, (255,255,255))

