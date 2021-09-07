import pygame
import math
import numpy
from scipy.spatial.transform import Rotation


def _draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
    """Helper function for drawing dashed lines. Thanks to https://codereview.stackexchange.com/a/70206"""


    class Point:
        # constructed using a normal tupple
        def __init__(self, point_t = (0,0)):
            self.x = float(point_t[0])
            self.y = float(point_t[1])
        # define all useful operators
        def __add__(self, other):
            return Point((self.x + other.x, self.y + other.y))
        def __sub__(self, other):
            return Point((self.x - other.x, self.y - other.y))
        def __mul__(self, scalar):
            return Point((self.x*scalar, self.y*scalar))
        def __div__(self, scalar):
            return Point((self.x/scalar, self.y/scalar))
        def __len__(self):
            return int(math.sqrt(self.x**2 + self.y**2))
        # get back values in original tuple format
        def get(self):
            return (self.x, self.y)


    origin = Point(start_pos)
    target = Point(end_pos)
    displacement = target - origin
    length = len(displacement)
    slope = displacement/length

    for index in range(0, length/dash_length, 2):
        start = origin + (slope *    index    * dash_length)
        end   = origin + (slope * (index + 1) * dash_length)
        pygame.draw.line(surf, color, start.get(), end.get(), width)


def _draw_dashed_lines(surf, color, points, width=1, dash_length=8):
    """Helper function for drawing dashed lines. Thanks to https://stackoverflow.com/a/66944050"""

    def draw_dashed_line(surf, color, p1, p2, prev_line_len, dash_length):
        dx, dy = p2[0]-p1[0], p2[1]-p1[1]
        if dx == 0 and dy == 0:
            return
        dist = math.hypot(dx, dy)
        dx /= dist
        dy /= dist

        step = dash_length*2
        start = (int(prev_line_len) // step) * step
        end = (int(prev_line_len + dist) // step + 1) * step
        for i in range(start, end, dash_length*2):
            s = max(0, start - prev_line_len)
            e = min(start - prev_line_len + dash_length, dist)
            if s < e:
                ps = p1[0] + dx * s, p1[1] + dy * s
                pe = p1[0] + dx * e, p1[1] + dy * e
                pygame.draw.line(surf, color, pe, ps, width)

    line_len = 0
    for i in range(1, len(points)):
        p1, p2 = points[i-1], points[i]
        dist = math.hypot(p2[0]-p1[0], p2[1]-p1[1])
        draw_dashed_line(surf, color, p1, p2, line_len, dash_length)
        line_len += dist



class Viewer:

    """This is a base-class for viewers in pygame."""


    def __init__(self, width, height, background_color):
        self.background_color = pygame.Color(background_color)
        self.surface = None
        self.static_surface = pygame.Surface((width, height))
        self.static_surface.fill(self.background_color)


    def reset(self):
        self.surface = self.static_surface.copy()


    # Drawing


    def static_circle(self, color, center, radius):
        pygame.draw.circle(self.static_surface, pygame.Color(color), center, radius)


    def circle(self, color, center, radius):
        pygame.draw.circle(self.surface, pygame.Color(color), center, radius)


    def static_line(self, color, start_pos, end_pos, width=1):
        pygame.draw.line(self.static_surface, pygame.Color(color), start_pos, end_pos, width=width)


    def line(self, color, start_pos, end_pos, width=1):
        pygame.draw.line(self.surface, pygame.Color(color), start_pos, end_pos, width=width)


    def static_lines(self, color, points, width=1):
        closed = False  # in teleop, rarely want lines filled in
        pygame.draw.lines(self.static_surface, pygame.Color(color), closed, points, width=width)


    def lines(self, color, points, width=1):
        closed = False  # in teleop, rarely want lines filled in
        pygame.draw.lines(self.surface, pygame.Color(color), closed, points, width=width)


    def static_dashed_line(self, color, start_pos, end_pos, width=1, dashed_length=10):
        _draw_dashed_line(self.static_surface, color, start_pos, end_pos, width, dash_length)


    def dashed_line(self, color, start_pos, end_pos, width=1, dashed_length=10):
        _draw_dashed_line(self.surface, color, start_pos, end_pos, width, dash_length)


    def static_dashed_lines(self, color, points, width=1, dash_length=10):
        _draw_dashed_lines(self.static_surface, color, points, width, dash_length)


    def dashed_lines(self, color, points, width=1, dash_length=10):
        _draw_dashed_lines(self.surface, color, points, width, dash_length)


    def _gen_rect_points(self, pos, width, height, rotation):
        corners = 0.5*numpy.array([
            [-1,  1, 1, -1],
            [-1, -1, 1,  1],
        ], dtype=float)
        t = numpy.diag(pos) @ numpy.ones(corners.shape, dtype=float)
        R = Rotation.from_euler('z', rotation, degrees=True).as_matrix()[:2,:2]
        S = numpy.diag([width, height])
        return (t + R @ S @ corners).round().astype(int).T.tolist()


    def static_rectangle(self, color, width, height, top_left_corner_pos, rotation=0):
        pygame.draw.polygon(self.static_surface, color, self._gen_rect_points(top_left_corner_pos, width, height, rotation))


    def rectangle(self, color, width, height, top_left_corner_pos, rotation=0):
        pygame.draw.polygon(self.surface, color, self._gen_rect_points(top_left_corner_pos, width, height, rotation))
