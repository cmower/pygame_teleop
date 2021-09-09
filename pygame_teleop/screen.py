import pygame
from .viewer import Viewer


class Screen(Viewer):

    """Main viewing screen implementation."""


    def __init__(self, config):

        # Initialize base class
        self.config = config
        Viewer.__init__(self, config['width'], config['height'], config['background_color'])

        # Setup screen
        self.screen = pygame.display.set_mode(self.static_surface.get_size())
        pygame.display.set_caption(self.config.get('caption', 'pygame_teleop'))
        self.clock = pygame.time.Clock()

        self._init_windows()


    def _init_windows(self):
        from .window import RobotEnvironment, Joystick, TimeSeries
        # Note, "from .window import *" throws syntax error. Will have
        # to update this when ever I add a new class in the window.py
        # script.
        self.windows = {}
        for name, config in self.config.get('windows', {}).items():
            class_type = config['type']
            self.windows[name] = eval(f'{class_type}(config)')
            print("Initialized window:", name)


    def reset(self):
        Viewer.reset(self)
        for window in self.windows.values():
            window.reset()


    def final(self, hz=None):
        self.screen.blit(self.surface, (0, 0))
        windows = sorted(self.windows.values(), key=lambda x: x.z_order)
        for window in windows:
            self.screen.blit(window.surface, window.config['origin'])
        pygame.display.flip()
        if isinstance(hz, int):
            self.clock.tick_busy_loop(hz)
