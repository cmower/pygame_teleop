import numpy
import pygame
pygame.joystick.init()

class _HumanInput:

    def __init__(self, d0=1, d1=1):
        assert abs(d0)==1 and abs(d1) == 1, "d0/d1 must be either -1 or 1"
        self._direction = [d0, d1]
        self._joy = pygame.joystick.Joystick(0)
        self._joy.init()
        assert self._joy.get_numaxes() > 1, "Your joystick does not have enough axes!"

    def get(self):
        self._joy.init()
        hraw = [d*self._joy.get_axis(i) for i, d in enumerate(self._direction)]
        h = pygame.math.Vector2(*hraw)
        return self._map(h)

    def _map(self, h):
        raise NotImplementedError("TODO")

    def button(self, idx):
        assert idx < self._joy.get_numbuttons(), "Not enough buttons!"
        self._joy.init()
        return self._joy.get_button(idx)

class HumanInputMode1(_HumanInput):

    """Isometric input"""

    def _map(self, h):
        scale = min(h.length(), 1)
        try:
            h.scale_to_length(scale)
        except ValueError:
            pass
        return numpy.array(h)
        
class HumanInputMode2(_HumanInput):

    """Car-like input"""

    def _map(self, h):
        return numpy.array([max(0, h.y), h.x])
