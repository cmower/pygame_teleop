import pygame
from pygame_teleop.screen import Screen


def main():

    # Setup
    config = {
        'caption': 'Drawing example',
        'width': 500,
        'height': 500,
        'background_color': 'darkslateblue',
        'windows':{
            'robotenv': {
                'origin': (10, 10),
                'width': 480,
                'height': 480,
                'background_color': 'white',
                'type': 'RobotEnvironment',
                'robotenv_width': 1.0,
                'robotenv_height': 1.0,
                'robotenv_origin_location': 'lower_left',
                'show_origin': True,
                'robots': {
                    'robot1': {
                        'show_path': False,
                        'robot_radius': 0.025,
                        'robot_color': 'black'
                    }
                }

            }
        }
    }
    screen = Screen(config)
    clock = pygame.time.Clock()
    draw_colors = ['red', 'green', 'blue']
    draw_color = None
    hz = 80
    draw = False
    running = True

    # Main loop
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    draw = True
                    draw_color = draw_colors[event.button-1]

                if event.type == pygame.MOUSEBUTTONUP:
                    draw = False

            pos = screen.windows['robotenv'].get_mouse_position()

            screen.reset()
            screen.windows['robotenv'].robots['robot1'].draw(pos)
            if draw:
                screen.windows['robotenv'].static_circle(
                    draw_color,
                    screen.windows['robotenv'].convert_position(pos),
                    screen.windows['robotenv'].convert_scalar(0.02),
                )
            screen.final()
            clock.tick(hz)
    except KeyboardInterrupt:
        pass

    pygame.quit()
    print("Goodbye")


if __name__ == '__main__':
    main()
