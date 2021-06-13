import pygame
import numpy

class _HumanInput:

    def __init__(self, d0=1, d1=1, button_keys=[]):
        assert abs(d0)==1 and abs(d1) == 1, "d0/d1 must be either -1 or 1"
        self._direction = [d0, d1]
        self._keys = {
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False
        }
        self._buttons = {key: False for key in button_keys}

    def reset(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key in self._keys.keys():
                    self._keys[e.key] = True
                if e.key in self._buttons.keys():
                    self._buttons[e.key] = True
            if e.type == pygame.KEYUP:
                if e.key in self._keys.keys():
                    self._keys[e.key] = False
                if e.key in self._buttons.keys():
                    self._buttons[e.key] = False
    def get(self):
        hori = float(self._keys[pygame.K_LEFT]) - float(self._keys[pygame.K_RIGHT])
        vert = float(self._keys[pygame.K_UP]) - float(self._keys[pygame.K_DOWN])
        h = pygame.math.Vector2([self._direction[0]*hori, self._direction[1]*vert])
        return self._map(h)

    def button(self):
        return self._buttons

class HumanInputMode1(_HumanInput):

    def _map(self, h):
        scale = min(h.length(), 1)
        try:
            h.scale_to_length(scale)
        except ValueError:
            pass
        return numpy.array(h)
    

class HumanInputMode2(_HumanInput):

    def _map(self, h):
        return numpy.array([h.y, h.x])
    
    
