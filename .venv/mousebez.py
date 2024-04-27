import random as rd
import numpy as np
import pyautogui as pag
import pytweening
from pyclick import HumanCurve

class MouseUtils:
    def move_to(self, destination: tuple, **kwargs):
        # sourcery skip: use-contextlib-suppress
        """
        Use Bezier curve to simulate human-like mouse movements.
        Args:
            destination: x, y tuple of the destination point
            destination_variance: pixel variance to add to the destination point (default 0)
        Kwargs:
            knotsCount: number of knots to use in the curve, higher value = more erratic movements
                        (default determined by distance)
            mouseSpeed: speed of the mouse (options: 'slowest', 'slow', 'medium', 'fast', 'fastest')
                        (default 'fast')
            tween: tweening function to use (default easeOutQuad)
        """
        offsetBoundaryX = kwargs.get("offsetBoundaryX", 100)
        offsetBoundaryY = kwargs.get("offsetBoundaryY", 100)
        knotsCount = kwargs.get("knotsCount", MouseUtils.__calculate_knots(destination))
        distortionMean = kwargs.get("distortionMean", 1)
        distortionStdev = kwargs.get("distortionStdev", 1)
        distortionFrequency = kwargs.get("distortionFrequency", 0.5)
        tween = kwargs.get("tweening", pytweening.easeOutQuad)
        mouseSpeed = kwargs.get("mouseSpeed", "fast")
        mouseSpeed = MouseUtils.__get_mouse_speed(mouseSpeed)

        dest_x = destination[0]
        dest_y = destination[1]

        start_x, start_y = pag.position()
        for curve_x, curve_y in HumanCurve(
            (start_x, start_y),
            (dest_x, dest_y),
            offsetBoundaryX=offsetBoundaryX,
            offsetBoundaryY=offsetBoundaryY,
            knotsCount=knotsCount,
            distortionMean=distortionMean,
            distortionStdev=distortionStdev,
            distortionFrequency=distortionFrequency,
            tween=tween,
            targetPoints=mouseSpeed,
        ).points:
            pag.moveTo((curve_x, curve_y))
            start_x, start_y = curve_x, curve_y

    def move_rel(self, x: int, y: int, x_var: int = 0, y_var: int = 0, **kwargs):
        """
        Use Bezier curve to simulate human-like relative mouse movements.
        Args:
            x: x distance to move
            y: y distance to move
            x_var: random upper-bound pixel variance to add to the x distance (default 0)
            y_var: random upper-bound pixel variance to add to the y distance (default 0)
        Kwargs:
            knotsCount: if right-click menus are being cancelled due to erratic mouse movements,
                        try setting this value to 0.
        """
        if x_var != 0:
            x += np.random.randint(-x_var, x_var)
        if y_var != 0:
            y += np.random.randint(-y_var, y_var)
        self.move_to((pag.position()[0] + x, pag.position()[1] + y), **kwargs)


    def __calculate_knots(destination: tuple):
        """
        Calculate the knots to use in the Bezier curve based on distance.
        Args:
            destination: x, y tuple of the destination point
        """
        # calculate the distance between the start and end points
        distance = np.sqrt((destination[0] - pag.position()[0]) ** 2 + (destination[1] - pag.position()[1]) ** 2)
        res = round(distance / 200)
        return min(res, 3)

    def __get_mouse_speed(speed: str) -> int:
        """
        Converts a text speed to a numeric speed for HumanCurve (targetPoints).
        """
        if speed == "slowest":
            return rd.randint(85, 100)
        elif speed == "slow":
            return rd.randint(65, 80)
        elif speed == "medium":
            return rd.randint(45, 60)
        elif speed == "fast":
            return rd.randint(20, 40)
        elif speed == "fastest":
            return rd.randint(10, 15)
        else:
            raise ValueError("Invalid mouse speed. Try 'slowest', 'slow', 'medium', 'fast', or 'fastest'.")

    def drag_to(self, x1, y1, x2, y2, **kwargs):
        """
        Simulates human-like mouse dragging from one point to another.
        Args:
            x1, y1: The x and y coordinates of the start point.
            x2, y2: The x and y coordinates of the destination point.
        Kwargs:
            Speed and other parameters that modify the behavior of the dragging.
        """
        # Calculate the destination variance if needed
        destination_variance = kwargs.get('destination_variance', 0)
        if destination_variance > 0:
            x2 += np.random.randint(-destination_variance, destination_variance)
            y2 += np.random.randint(-destination_variance, destination_variance)


        # Use the existing moveTo functionality but hold down the left mouse button
        pag.mouseDown(x=x1, y=y1)

        # Call the moveTo method to simulate human-like movement to the destination while the button is pressed
        self.move_to((x2, y2), **kwargs)

        # Release the mouse button at the destination
        pag.mouseUp(x=x2, y=y2)

    def rnd(self, rang):
        start_x, start_y = pag.position()
        x = rd.randint(rang,rang)
        y = rd.randint(rang,rang)
        self.move_to((start_x+x, start_y+y), mouseSpeed='slow', knotsCount=1)



'''
#Example
mouse = MouseUtils()
cords = (500, 500)
mouse.move_to(cords, mouseSpeed='slow', knotsCount=1)
'''