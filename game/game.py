import pygame
from pygame.locals import *

import time
import gmap
import player

class Game():

    def __init__(self, config):
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 18)
       
        self.size=config.get('resolution', (800,600))
        self.screen=pygame.display.set_mode(self.size)
        self.color_key=config.get('color_key', (100,20,30))

        self.done = False
        self.frame_length = 1./60

        self.event_objects = []
        self.tick_objects = []
        self.render_objects = []
        self.modal = None

        self.map = gmap.Map(self, config)
        self.player = player.Player(self, config)

        for tlist in [self.tick_objects, self.render_objects]:
            tlist.append(self.map)
            tlist.append(self.player)

        self.layers = {}
        self.get_screen(0)

    def get_screen(self, key):
        if not key in self.layers.keys():
            self.layers[key] = pygame.Surface(self.size)
            self.layers[key].set_colorkey(self.color_key)
        return self.layers[key]

    def clear_screens(self):
        for screen in self.layers.values():
            screen.fill(self.color_key)

    def run(self):
        while not self.done:
            start_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    self.done = True
                elif self.modal != None:
                    self.modal.event(event)
                elif self.player.event(event):
                    continue
                elif self.map.event(event):
                    continue
                else:
                    for obj in self.event_objects:
                        if obj.event(event): continue

            for obj in self.tick_objects:
                result = obj.tick()

            self.screen.fill((0,0,0))
            self.clear_screens()

            for obj in self.render_objects:
                obj.render()

            for key in sorted(self.layers.keys()):
                self.screen.blit(self.layers[key], (0,0))

            text = self.font.render('{}'.format(self.player.jump_count), True, (255,255,255))
            self.screen.blit(text, (0,0))

            pygame.display.flip()

            extra_time = self.frame_length - (time.time()-start_time)
            if extra_time > 0:
                time.sleep(extra_time)

