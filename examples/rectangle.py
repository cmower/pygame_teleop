import numpy
import pygame
import math
from math import cos, sin
from pygame_teleop.screen import Screen

pi = numpy.pi

def main():

    # Setup config, could be easily loaded from a yaml file
    config = {
        'caption': 'Example for pygame_teleop',
        'width': 500,
        'height': 500,
        'background_color': 'white',
    }

    # Setup
    screen = Screen(config)
    running = True
    hz = 30
    dt = 1.0/float(hz)
    max_vel = 0.1
    x_radius = 40
    omega = -float(50)  # deg/sec
    r = 0.0
    clock = pygame.time.Clock()

    # Main loop
    try:
        while running:

            # Check that user didn't quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update robot and box
            t = float(pygame.time.get_ticks())*0.001
            b = 0.5*500*numpy.ones(2) + 100*numpy.array([cos(t + pi), sin(t + pi)])
            r += omega*dt

            # Update screen
            screen.reset()
            screen.rectangle('red', 100, 40, b, r)
            screen.circle('black', b, 10)
            screen.final()

            # Tick
            clock.tick(hz)

    except KeyboardInterrupt:
        pass

    pygame.quit()
    print("Goodbye")


if __name__ == '__main__':
    main()
