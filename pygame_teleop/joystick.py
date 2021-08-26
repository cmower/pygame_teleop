import math
import pygame
pygame.joystick.init()


class Joystick:

    """Joystick interface. Note, this assumes only one joystick is attached."""


    def __init__(self, jid=0):
        self.joy = pygame.joystick.Joystick(jid)
        self.joy_id = self.joy.get_id()
        self.numaxes = self.joy.get_numaxes()
        self.numbuttons = self.joy.get_numbuttons()
        print("Initialized joystick:", self.joy.get_name())


    @staticmethod
    def isometric(axes):
        a0, a1 = axes
        anorm = math.sqrt(a0**2 + a1**2)
        ascale = min(1.0, anorm)
        atheta = math.atan2(a1, a0)
        return (ascale*math.cos(atheta), ascale*math.sin(atheta))


    def reset(self):
        self.joy.init()

    def get_axis(self, axis_number):
        return self.joy.get_axis(axis_number)


    def get_axes(self):
        return [self.joy.get_axis(axis_number) for axis_number in range(self.numaxes)]


    def get_button(self, button):
        return self.joy.get_button(button)


    def get_buttons(self):
        return [self.joy.get_button(button) for button in range(self.numbuttons)]


    def get_buttons_down(self, event_list):
        buttons = [False]*self.numbuttons
        for event in event_list:
            if event.type == pygame.JOYBUTTONDOWN:
                buttons[joy.button] = True
        return buttons


    def get_buttons_up(self, event_list):
        buttons = [False]*self.numbuttons
        for event in event_list:
            if event.type == pygame.JOYBUTTONUP:
                buttons[joy.button] = True
        return buttons
