import pygame
from .viewer import Viewer

"""
Window implementations.

Notes
Every time you add a new Window sub-class, you need to update the
Screen._init_windows method in the screen.py script - this is just a
hard fact of life!
"""

class Window(Viewer):


    def __init__(self, config):

        # Initialize base class
        self.config = config
        Viewer.__init__(self, config['width'], config['height'], config['background_color'])

        # Initialize window
        self._post_init()


    def _post_init(self):
        pass


class RobotEnvironment(Window):


    def _post_init(self):

        # Check dimensions
        tol = 1e-5
        w, h = float(self.config['robotenv_width']), float(self.config['robotenv_height']),
        W, H = float(self.static_surface.get_width()), float(self.static_surface.get_height())
        assert abs((w/h) - (W/H)) < tol, "aspect ratio is not consistent between pygame window and robot environment"

        self.robotenv_origin_location = self.config.get('robotenv_origin_location', 'upper_left')
        self._convert_position = getattr(self, f'_convert_position_{self.robotenv_origin_location}')
        if self.robotenv_origin_location == 'upper_right':
            raise NotImplementedError("since this error was raised, there is now a need to implement upper_right use-case, see RobotEnvironment class.")


    def _convert_position_upper_left(self, x, y, w, h, W, H):
        return W*x/w, H*y/h


    def _convert_position_lower_left(self, x, y, w, h, W, H):
        return W*x/w, (H/h)*(h-y)

    def _convert_position_lower_right(self, x, y, w, h, W, H):
        return (W/w)*(w-x), (H/h)*(h-y)


    def convert_position(self, pos):
        X, Y = self._convert_position(  # see _post_init re _convert_position
            float(pos[0]), float(pos[1]),
            float(self.config['robotenv_width']), float(self.config['robotenv_height']),
            float(self.static_surface.get_width()), float(self.static_surface.get_height())
        )
        return int(round(X)), int(round(Y))


class Joystick(Window):


    def _post_init(self):

        # Check dimensions
        assert self.config['width'] == self.config['height'], "width and height must be the same for Joystick"

        # Compute tip radius, mid width, and width
        D = float(self.config['width'])
        self.tip_radius = 0.075*D  # d0
        self.mid_width = D - 2*self.tip_radius  # d1
        self.joy_width = int(round(0.5*self.tip_radius))

        # Setup joystick base
        self.joy_color = self.config.get('joy_color', 'darkgrey')
        self.middle = (int(round(D/2.0)), int(round(D/2.0)))
        self.static_circle(self.joy_color, self.middle, int(round(self.tip_radius)))

        if self.config.get('flip_a0', False):
            self._flip_a0 = self._do_flip
        else:
            self._flip_a0 = self._dont_flip

        if self.config.get('flip_a1', False):
            self._flip_a1 = self._do_flip
        else:
            self._flip_a1 = self._dont_flip

        # Get tip color
        self.joy_tip_color = pygame.Color(self.config.get('joy_tip_color', 'red'))


    def _dont_flip(self, a):
        return a


    def _do_flip(self, a):
        return -1.0 * a


    def draw(self, axes):

        # Setup, see _post_init re _flip_a0 and _flip_a1
        a0 = self._flip_a0(axes[0])
        a1 = self._flip_a1(axes[1])

        # Compute location
        x = 0.5*(a0 + 1.0)
        y = 0.5*(a1 + 1.0)
        X = int(round(self.tip_radius + x*self.mid_width))
        Y = int(round(self.tip_radius + y*self.mid_width))
        pos = (X, Y)

        # Draw
        self.line(self.joy_color, self.middle, pos, self.joy_width)
        self.circle(self.joy_tip_color, pos, self.tip_radius)
