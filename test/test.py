import sys
import numpy
import traceback
import pygame
from pygame_teleop.window import Window
from pygame_teleop.human_input import HumanInputMode1 as HumanInputJoystick
from pygame_teleop.keyboard import HumanInputMode1 as HumanInputKeyboard


def main():

    #### USER INPUT
    robot_radius = 0.05
    hz = 30
    robot = numpy.array([0.5, 0.5])
    max_vel = 0.1
    window_width = 500
    #### USER INPUT

    # Setup
    try:
        d0, d1 = 1, 1
        use_keyb = False
        human = HumanInputJoystick(d0, d1)
    except pygame.error:
        d0, d1 = -1, -1
        use_keyb = True
        human = HumanInputKeyboard(d0, d1, button_keys=[pygame.K_SPACE])
    dt = 1.0/float(hz)
    running = True
    window = Window(window_width)
    rval = 0

    # Main loop
    try:
        
        while running:

            events = window.events()

            if not use_keyb:
                b = human.button(0)
                h = human.get()
            else:
                human.reset(events)
                b = human.button()[pygame.K_SPACE]
                h = human.get()

            # Update robot
            robot += max_vel*dt*h
            robot = numpy.clip(robot, 0, 1)

            # Update window
            window.reset()
            window.robot(robot, robot_radius)
            window.update(hz)

            # Quit?
            user_quit = window.did_user_quit(events) or b
            running = not user_quit
            
    except KeyboardInterrupt:
        pass
    
    except:
        print("-"*70)
        traceback.print_exc(file=sys.stdout)
        print("-"*70)
        rval = 1
    finally:
        window.shutdown()

    return rval

if __name__ == '__main__':
    sys.exit(main())
