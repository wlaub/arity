import pygame
from pygame.locals import *


class Player():

    xvel = 120

    def __init__(self, game, config):
        self.g = game
        self.pos = config.get('start_pos', [400,300])
        self.vel = [0,0]
        self.jump = 0
        self.jump_tol = 0
        self.jump_count = 0
        self.do_land = False

    def event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_z:
                self.g.map.do_jump(self)

    def can_jump(self):
        return abs(self.vel[1]) <= self.jump_tol
        return self.jump == 0

    def land(self):
        self.do_land = True
        self.jump = 0
        self.jump_count=0

    def tick(self, delta):
        keys = pygame.key.get_pressed()
        xvel = self.xvel
        if keys[K_LEFT]:
            if self.jump > 0:
                self.vel[0] -= xvel/8.
            else:
                self.vel[0] = -xvel
        elif keys[K_RIGHT]:
            if self.jump > 0:
                self.vel[0] += xvel/8.
            else:
                self.vel[0] = xvel

        if self.vel[0] > xvel: self.vel[0] = xvel
        if self.vel[0] < -xvel: self.vel[0] = -xvel

        pos = list(self.pos)

        self.g.map.do_player(self, delta)

        if self.do_land:
            self.do_land=False
            self.vel[0] = 0
        #TODO better landing management?
        dvel = list(map(lambda x: x[0]-x[1], zip(pos, self.pos)))
        print(dvel)

    def render(self):
        screen = self.g.get_screen(0)
        ipos = list(map(int, self.pos))

        rad = min(abs(self.vel[1]), 10)
        a = int(255*(rad/10.))

        pygame.draw.circle(screen, (a,a,a), ipos, int(rad))

        if self.can_jump():
            pygame.draw.circle(screen, (255,255,255), ipos, 5)

        screen.set_at(ipos, (255,255,255))

