import pygame
import numpy
from scipy.interpolate import interp1d
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


class EnvironmentObject:

    def __init__(self, robotenv, config):
        self.robotenv = robotenv
        self.config = config


class Robot(EnvironmentObject):


    def __init__(self, robotenv, config):
        EnvironmentObject.__init__(self, robotenv, config)
        self.previous_position = None
        self.robot_radius = robotenv.convert_scalar(self.config['robot_radius'])
        self.show_path = self.config.get('show_path', True)
        self.path_width = self.config.get('path_width', 1)
        self.path_color = self.config.get('path_color', 'black')  # NOTE, if you can't see the path, is your background black?


    def draw(self, x):
        x_use = self.robotenv.convert_position(x)
        if (self.previous_position is not None) and self.show_path:
            self.robotenv.static_line(self.path_color, self.previous_position, x_use, self.path_width)
        self.robotenv.circle(self.config['robot_color'], x_use, self.robot_radius)
        self.previous_position = x_use


class RobotEnvironment(Window):

    rotation_direction = {
        'lower_left': -1.0,
        'upper_left': 1.0,
        'lower_right': 1.0,
    }


    def _post_init(self):

        # Check dimensions
        tol = 1e-5
        w, h = float(self.config['robotenv_width']), float(self.config['robotenv_height']),
        W, H = float(self.static_surface.get_width()), float(self.static_surface.get_height())
        assert abs((w/h) - (W/H)) < tol, "aspect ratio is not consistent between pygame window and robot environment"
        self.k = W/w  # scaling factor
        self.w = w
        self.h = h
        self.W = W
        self.H = H

        self.robotenv_origin_location = self.config.get('robotenv_origin_location', 'upper_left')
        self._convert_position = getattr(self, f'_convert_position_{self.robotenv_origin_location}')
        self._revert_position = getattr(self, f"_revert_position_{self.robotenv_origin_location}")
        if self.robotenv_origin_location == 'upper_right':
            raise NotImplementedError("since this error was raised, there is now a need to implement upper_right use-case, see RobotEnvironment class.")

        # Setup robots
        self.robots = {name: Robot(self, config) for name, config in self.config.get('robots', {}).items()}

        # Include origin
        if self.config.get('show_origin', False):
            axis_scale = 0.1
            origin_center = self.convert_position((0, 0))
            line_width = self.convert_scalar(w*0.01)
            self.static_line('red', origin_center, self.convert_position((w*axis_scale, 0)), width=line_width)  # x axis
            self.static_line('green', origin_center, self.convert_position((0, h*axis_scale)), width=line_width)  # y axis
            self.static_circle('blue', origin_center, self.convert_scalar(w*0.0175))


    def _convert_position_upper_left(self, x, y):
        return self.W*x/self.w, self.H*y/self.h


    def _revert_position_upper_left(self, X, Y):
        return self.w*X/self.W, self.h*Y/self.H


    def _convert_position_lower_left(self, x, y):
        return self.W*x/self.w, (self.H/self.h)*(self.h-y)


    def _revert_position_lower_left(self, X, Y):
        return self.w*X/self.W, self.h*(1.0-Y/self.H)


    def _convert_position_lower_right(self, x, y):
        return (self.W/self.w)*(self.w-x), (self.H/self.h)*(self.h-y)


    def _revert_position_lower_right(self, x, y):
        return self.w*(1.0-X/self.W), (self.H/self.h)*(self.h-y)


    def convert_scalar(self, s):
        return int(round(self.k*float(s)))


    def convert_position(self, pos):
        X, Y = self._convert_position(  # see _post_init re _convert_position
            float(pos[0]), float(pos[1]),
        )
        return int(round(X)), int(round(Y))


    def revert_position(self, pos):
        return self._revert_position(float(pos[0]), float(pos[1]))


    def convert_path(self, path):

        # Extract x, y and ensure float type
        x = path[0,:].astype(float)
        y = path[1,:].astype(float)

        # Convert position
        X, Y = self._convert_position(x, y)

        return numpy.stack((X, Y)).round().astype(int)


    def draw_path(self, color, path, width=1, dashed=False):
        if dashed:
            self.dashed_lines(color, self.convert_path(path).T.tolist(), width)
        else:
            self.lines(color, self.convert_path(path).T.tolist(), width)

    def draw_box(self, color, width, height, center_pos, rotation=0):
        r = self.rotation_direction[self.robotenv_origin_location]*numpy.rad2deg(rotation)
        self.rectangle(color, self.convert_scalar(width), self.convert_scalar(height), self.convert_position(center_pos), r)


    def get_mouse_position(self):
        xscreen, yscreen = pygame.mouse.get_pos()
        return self.revert_position((xscreen - self.config['origin'][0], yscreen - self.config['origin'][1]))


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


class TimeSeries(Window):


    def _post_init(self):
        self.n = self.config.get('n', 50)
        if self.config.get('show_axis', True):
            axis_width = self.config.get('axis_width', 1)
            axis_color = self.config.get('axis_color', 'black')
            self.static_line(axis_color, (0, self.config['height']/2), (self.config['width'], self.config['height']/2), axis_width)
            tp = float(self.config['tp'])
            tf = float(self.config['tf'])
            W = float(self.config['width'])
            M = int(round(tp*W/(tp+tf)))
            self.static_line(axis_color, (M, 0), (M, self.config['height']), axis_width)


    def plot_point(self, t, y, color, radius=2):

        # Convert to pygame coordinates
        t = (t + self.config['tp']) / (self.config['tp'] + self.config['tf'])
        T = int(round(self.config['width']*t))

        y = (y + abs(self.config['y_lo'])) / (abs(self.config['y_lo']) + abs(self.config['y_up']))
        Y = int(round((self.config['height']*y)))

        # Draw
        self.circle(color, (T, Y), radius)


    def plot_line(self, t, y, color, line_width=1, dashed=False, dash_length=10):

        # Interpolate data
        yfun = interp1d(t, y, bounds_error=False, fill_value='extrapolate')

        # Downsample data
        t_lo = max(t.min(), -self.config['tp'])
        t_up = min(t.max(), self.config['tf'])
        t_use = numpy.linspace(t_lo, t_up, self.n)
        y_use = yfun(t_use)

        # Convert to pygame coordinates
        t_use = (t_use + self.config['tp']) / (self.config['tp'] + self.config['tf'])
        T = (self.config['width']*t_use).round().astype(int)

        y_use = (y_use + abs(self.config['y_lo'])) / (abs(self.config['y_lo']) + abs(self.config['y_up']))
        Y = (self.config['height']*y_use).round().astype(int)

        points = numpy.stack((T, Y)).T.tolist()

        # Draw
        if dashed:
            self.dashed_lines(color, points, width=line_width, dash_length=dash_length)
        else:
            self.lines(color, points, width=line_width)
