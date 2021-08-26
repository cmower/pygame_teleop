import pygame



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
