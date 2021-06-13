import sys
import numpy
import traceback
from pygame_teleop.window import Window
from pygame_teleop.human_input import HumanInputMode1


def main():

    #### USER INPUT
    joy_d0, joy_d1 = 1, 1
    robot_radius = 0.05
    hz = 30
    robot = numpy.array([0.5, 0.5])
    max_vel = 0.1
    window_width = 500
    #### USER INPUT

    # Setup
    human = HumanInputMode1(joy_d0, joy_d1)
    dt = 1.0/float(hz)
    running = True
    window = Window(window_width)
    rval = 0

    # Main loop
    try:
        
        while running:

            # Update robot
            robot += max_vel*dt*human.get()
            robot = numpy.clip(robot, 0, 1)

            # Update window
            window.reset()
            window.robot(robot, robot_radius)
            window.update(hz)

            # Quit?
            user_quit = window.did_user_quit(window.events()) or human.button(0)
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
