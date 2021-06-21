import pygame
from math import atan2, sin, cos, pi
pygame.init()

BLACK = pygame.Color('black')
WHITE = pygame.Color('white')
BLUE = pygame.Color('blue')

class Window:

    def __init__(self, width, bg_color=WHITE):

        # Setup
        self.width = width
        self._screen_dimensions = (self.width, self.width)

        # Setup screen
        self._screen = pygame.display.set_mode(self._screen_dimensions)
        self._static_screen = pygame.Surface(self._screen_dimensions)
        self._static_screen.fill(bg_color)

        # Setup clock
        self._clock = pygame.time.Clock()

    def _to_pg_coords(self, v):
        return float(self.width)*pygame.math.Vector2(tuple(v))

    def static_line(self, start_pos, end_pos, width=1, color=BLACK):
        pygame.draw.line(
            self._static_screen,
            color,
            self._to_pg_coords(start_pos),
            self._to_pg_coords(end_pos),
            width,
        )

    def static_lines(self, points, width=1, color=BLACK):
        pygame.draw.lines(
            self._static_screen,
            color,
            False,
            [self._to_pg_coords(p) for p in points],
            width,
        )

    def static_circle(self, center, radius, color=BLACK):
        pygame.draw.circle(
            self._static_screen,
            color,
            self._to_pg_coords(center),
            float(self.width)*radius,
        )

    def events(self):
        return pygame.event.get()

    def did_user_quit(self, events):
        return any(e.type == pygame.QUIT for e in events)

    def get_mouse_pos(self):
        x, y = pygame.mouse.get_pos()
        return float(x)/float(self.width), float(y)/float(self.width)

    def reset(self):
        self._screen.blit(self._static_screen, (0, 0))

    def line(self, start_pos, end_pos, width=1, color=BLACK):
        pygame.draw.line(
            self._screen,
            color,
            self._to_pg_coords(start_pos),
            self._to_pg_coords(end_pos),
            width,
        )

    def lines(self, points, width=1, color=BLACK):
        pygame.draw.lines(
            self._screen,
            color,
            False,
            [self._to_pg_coords(p) for p in points],
            width,
        )

    def cirle(self, center, radius, color=BLACK):
        pygame.draw.circle(
            self._screen,
            color,
            self._to_pg_coords(center),
            float(self.width)*radius,
        )

    def robot(self, position, radius, color=BLUE):
        pygame.draw.circle(
            self._screen,
            color,
            self._to_pg_coords(position),
            float(self.width)*radius,
        )

    def update(self, hz):
        pygame.display.flip()
        self._clock.tick(hz)

    def shutdown(self):
        pygame.quit()
