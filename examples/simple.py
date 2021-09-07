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
        'background_color': 'darkslateblue',
        'windows': {
            'robotenv': {
                'origin': (10, 10),
                'width': 480,
                'height': 480,
                'background_color': 'white',
                'type': 'RobotEnvironment',
                'robotenv_width': 1.0,
                'robotenv_height': 1.0,
                'robotenv_origin_location': 'lower_left',
                'robots': {
                    'robot1': {
                        'robot_radius': 0.025,
                        'show_path': False,
                        'robot_color': 'blue',
                    },
                    'box_center': {
                        'robot_radius': 0.025,
                        'show_path': False,
                        'robot_color': 'black',
                    }
                }
            }
        }
    }

    # Setup
    screen = Screen(config)
    running = True
    hz = 30
    dt = 1.0/float(hz)
    max_vel = 0.1
    x_radius = 40
    omega = numpy.deg2rad(190)
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
            x = 0.5*numpy.ones(2) + 0.2*numpy.array([cos(t), sin(t)])
            b = 0.5*numpy.ones(2) + 0.2*numpy.array([cos(t + pi), sin(t + pi)])
            r += omega*dt

            # Update screen
            screen.reset()
            screen.windows['robotenv'].robots['robot1'].draw(x)
            screen.windows['robotenv'].draw_box('red', 0.2, 0.1, b, r)
            screen.windows['robotenv'].robots['box_center'].draw(b)
            screen.final()

            # Tick
            clock.tick(hz)

    except KeyboardInterrupt:
        pass

    pygame.quit()
    print("Goodbye")


if __name__ == '__main__':
    main()
