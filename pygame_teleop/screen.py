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

        self._init_windows()


    def _init_windows(self):
        from .window import RobotEnvironment, Joystick, TimeSeries
        # Note, "from .window import *" throws syntax error. Will have
        # to update this when ever I add a new class in the window.py
        # script.
        self.windows = {}
        for name, config in self.config['windows'].items():
            class_type = config['type']
            self.windows[name] = eval(f'{class_type}(config)')
            print("Initialized window:", name)


    def reset(self):
        Viewer.reset(self)
        for window in self.windows.values():
            window.reset()


    def final(self):
        self.screen.blit(self.surface, (0, 0))
        for window in self.windows.values():
            self.screen.blit(window.surface, window.config['origin'])
        pygame.display.flip()
