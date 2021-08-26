import numpy
import pygame
from pygame_teleop.screen import Screen
from pygame_teleop.joystick import Joystick


def main():

    # Setup config, could be easily loaded from a yaml file
    w0 = 20
    w1 = 500
    w2 = 300
    config = {
        'caption': 'Example for pygame_teleop',
        'width': 3*w0+w1+w2,
        'height': 2*w0+w2,
        'background_color': 'darkslateblue',
        'windows': {
            'joy': {
                'origin': (2*w0 + w1, w0),
                'width': w2,
                'height': w2,
                'background_color': 'white',
                'type': 'Joystick',
                'joy_color': 'darkgrey',
                'flip_a0': False,
                'flip_a1': False,
                'joy_tip_color': 'red',
            },
            'robotenv': {
                'origin': (w0, w0),
                'width': w1,
                'height': w2,
                'background_color': 'white',
                'type': 'RobotEnvironment',
                'robotenv_width': 1.0,
                'robotenv_height': float(w2)/float(w1),
                'robotenv_origin_location': 'lower_left',
            }
        }
    }

    # Setup
    screen = Screen(config)
    joy = Joystick()
    running = True
    hz = 30
    dt = 1.0/float(hz)
    max_vel = 0.1
    x = numpy.array([0.5, 0.5*float(w2)/float(w1)], dtype=float)
    x_radius = 40
    clock = pygame.time.Clock()

    # Main loop
    try:
        while running:

            # Check that user didn't quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update user input
            joy.reset()
            axes = joy.get_axes()[:2]
            if joy.get_button(0):
                running = False

            # Parse input
            h = numpy.array(joy.isometric(axes), dtype=float)
            h[1] *= -1

            # Update robot
            x += dt*h*max_vel
            x = numpy.clip(x, [0, 0], [1, float(w2)/float(w1)])
            x_pg = screen.windows['robotenv'].convert_position(x)

            # Update screen
            screen.reset()
            screen.windows['joy'].draw(axes)
            screen.windows['robotenv'].circle('blue', x_pg, x_radius)
            screen.final()

            # Tick
            clock.tick(hz)

    except KeyboardInterrupt:
        pass

    pygame.quit()
    print("Goodbye")


if __name__ == '__main__':
    main()
