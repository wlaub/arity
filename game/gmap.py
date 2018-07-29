import pygame
from pygame.locals import *

import itertools, math
from array import array

class Map():
    
    def __init__(self, game, config):
        self.g = game
        self.rooms = []
        Tile.size = tuple(map(lambda x: int(x[0]/x[1]), zip(self.g.size, Room.size)))
        self.active_room = Room(game, config)


    def do_player(self, player):
        player.vel[1] += self.active_room.grav
        player.pos = list(map(lambda x: x[0]+x[1], zip(player.pos, player.vel)))

        player.jump_count += 1
        f = 550
        if player.pos[1] > f:
            player.jump = 0
            player.pos[1] = f
            player.vel[0] = 0
            player.vel[1] = 0
            player.jump_count = 0

    def do_jump(self, player):
        if player.can_jump():
            jvel, jtol = self.active_room.get_jump_vel(player)
            if jvel != None:
                self.active_room.jumpseq.play(player.jump)               
                player.jump+= 1
                player.vel[1] = jvel
                player.jump_tol = jtol
                player.jump_count = 0




    def event(self, event):
        pass

    def tick(self):
        pass

    def render(self):
        self.active_room.render()


class Room():
    size = (40,30)

    grav = .1

    def __init__(self, game, config):
        self.g = game

        self.tiles = {(x,y): Tile((x,y)) for x,y in itertools.product(range(self.size[0]), range(self.size[1]))}

        self.jumpseq = JumpSequence()

        #temporary
        self.tiles[(0,0)].color = 1
        for x in range(self.size[0]):
            self.tiles[(x, self.size[1]-1)].color= 2
        for tile in self.tiles.values():
            tile.pre_render()

    def get_jump_vel(self, player):
        return self.jumpseq.get_vel(self.grav, player.jump)

    def event(self, event):
        pass

    def tick(self):
        pass

    def render(self):
        for tile in self.tiles.values():
            tile.render(self.g.get_screen(tile.layer))

class Tile():
    colors = {
    0: (0,0,0),
    1: (255,0,0),
    2: (0,255,0),
    3: (0,0,255),
    4: (255,255,255)
    }
    def __init__(self, pos):
        self.pos = tuple(map(lambda x: x[0]*x[1], zip(pos, self.size)))
        self.rect = (
                (self.pos[0], self.pos[1]),
                (self.size[0], self.size[1]))
        a = .1
        self.inner_rect = (
                (self.size[0]*a, self.size[1]*a),
                (self.size[0]*(1-2*a), self.size[1]*(1-2*a)))


        self.color = 0
        self.layer = 0

        self.pre_render()

    def pre_render(self):
        scale = 2**self.layer
        self.image = pygame.Surface(self.size)

        self.image.fill(list(map(lambda x: x/scale, self.colors[self.color])) )
        self.image.fill((0,0,0), self.inner_rect)


    def render(self, screen):
        if self.color == 0: return
        screen.blit(self.image, self.pos)


class JumpSequence():
    def __init__(self):
        scale = 15
        self.times = [2, 1, 2, 2, 4]
        self.notes = [4, 7, 9, 11, 7]
        self.times = list(map(lambda x: x*scale, self.times))

        import numpy as np

        sample = lambda x: int(10000* (math.exp(-x[0]/10000.)) * (math.sin(.04*x[0]*2**(x[1]/12.))) )

        self.sounds = [
        pygame.mixer.Sound(
            array=np.array(
                [[sample((i, x[0])), sample((i, x[0], x[1]))]
                    for i in range(int(x[1]*44100/60))],
                dtype=np.int16
                )
            )
        for x in zip(self.notes, self.times)]

    def play(self, i):
        self.sounds[i].play()

    def get_vel(self, grav, i):
        if i >= len(self.times): return None, None
        vel = -grav*self.times[i]
        tol = grav*4

        return vel, tol


