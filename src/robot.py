import math
import time
from PIL import ImageGrab

class Robot:
    def __init__(self, gui, arena, link_length1=200, link_length2=200):
        self.gui = gui
        self.arena = arena
        self.link_length1 = link_length1
        self.link_length2 = link_length2
        self.theta1 = 0
        self.theta2 = 0
        self.joint1 = (self.gui.width // 2, self.gui.height // 2)  # Initial position of the first joint (base)
        self.joint2 = (self.joint1[0] + link_length1, self.joint1[1])  # Initial position of the second joint
        self.end_effector = (self.joint2[0] + link_length2, self.joint2[1])  # Initial position of the end effector
        self.max_theta1 = 90
        self.min_theta1 = -110
        self.max_theta2 = 160
        self.min_theta2 = 0
        self.update_gui()

    def inverse_kinematics(self, target):
        x, y = target
        x -= self.gui.width // 2  # Adjust for the center of the canvas
        y = self.gui.height // 2 - y  # Adjust for the center of the canvas and invert y-axis
        l1, l2 = self.link_length1, self.link_length2

        # Calculate the inverse kinematics
        cos_theta2 = (x ** 2 + y ** 2 - l1 ** 2 - l2 ** 2) / (2 * l1 * l2)
        cos_theta2 = min(1, max(-1, cos_theta2))  # Clamp to the range [-1, 1]
        sin_theta2 = math.sqrt(1 - cos_theta2 ** 2)
        theta2 = math.atan2(sin_theta2, cos_theta2)

        k1 = l1 + l2 * cos_theta2
        k2 = l2 * sin_theta2
        theta1 = math.atan2(y, x) - math.atan2(k2, k1)

        # Convert to degrees
        theta1 = math.degrees(theta1)
        theta2 = math.degrees(theta2)

        return math.radians(theta1), math.radians(theta2)

    def forward_kinematics(self, theta1, theta2):
        l1, l2 = self.link_length1, self.link_length2
        x1 = l1 * math.cos(theta1)
        y1 = l1 * math.sin(theta1)
        x2 = x1 + l2 * math.cos(theta1 + theta2)
        y2 = y1 + l2 * math.sin(theta1 + theta2)

        self.joint2 = (self.gui.width // 2 + x1, self.gui.height // 2 - y1)  # Adjust for the center of the canvas and invert y-axis
        self.end_effector = (self.gui.width // 2 + x2, self.gui.height // 2 - y2)  # Adjust for the center of the canvas and invert y-axis

        return [(self.gui.width // 2, self.gui.height // 2), self.joint2, self.end_effector]

    def move(self, target, step_name=""):
        theta1, theta2 = self.inverse_kinematics(target)
        if theta1 is None or theta2 is None:
            return [], []  # If the target is not reachable

        theta1_deg = math.degrees(theta1)
        theta2_deg = math.degrees(theta2)
        if not (self.min_theta1 <= theta1_deg <= self.max_theta1 and self.min_theta2 <= theta2_deg <= self.max_theta2):
            print(f"Target ({target}) results in out of bounds angles: theta1={theta1_deg}, theta2={theta2_deg}")
            return [], []

        # Generate detailed steps for animation and recording
        steps = 2  # Increased the number of steps for smoother animation
        # steps = 2  # Increased the number of steps for smoother animation
        detailed_steps = []
        thetas = []
        for i in range(1, steps + 1):
            inter_theta1 = self.theta1 + (theta1 - self.theta1) * i / steps
            inter_theta2 = self.theta2 + (theta2 - self.theta2) * i / steps
            joints = self.forward_kinematics(inter_theta1, inter_theta2)
            detailed_steps.append(joints)
            thetas.append((math.degrees(inter_theta1), math.degrees(inter_theta2)))
            self.update_gui(joints)
            self.gui.root.update()  # Update the GUI to show the animation

            # Capture screenshots for specific steps
            # if i in {1, 6, 11, 20}:
            #     x1, y1 = 0, 0
            #     x2, y2 = self.gui.width, self.gui.height
            #     ImageGrab.grab(bbox=(x1, y1, x2, y2)).save(f'./pictures/{step_name}_step_{i}.png')

            if i in {1}:
                x1, y1 = 0, 0
                x2, y2 = self.gui.width, self.gui.height
                ImageGrab.grab(bbox=(x1, y1, x2, y2)).save(f'./pictures/{step_name}_step_{i}.png')

            time.sleep(0.05)  # Reduced delay for smoother animation

            # Check and remove targets if reached
            if self.arena.check_target_reached(self.end_effector_position):
                self.arena.remove_target(self.end_effector_position)
                self.update_gui(joints)  # Update GUI after removing target

        # Update the robot's angles to the final angles
        self.theta1, self.theta2 = theta1, theta2
        return detailed_steps, thetas

    def update_gui(self, joints=None):
        self.gui.clear_canvas()
        if joints is None:
            joints = [(self.gui.width // 2, self.gui.height // 2), self.joint2, self.end_effector]
        self.gui.draw_robot(joints)
        self.arena.draw_boundaries()
        self.arena.draw_targets()

    @property
    def end_effector_position(self):
        return self.end_effector
