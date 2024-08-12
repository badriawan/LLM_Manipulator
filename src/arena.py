import math


class Target:
    def __init__(self, position, color):
        self.position = position
        self.color = color


class Arena:
    def __init__(self, gui, boundaries):
        self.gui = gui
        self.boundaries = boundaries
        self.targets = []
        self.draw_boundaries()

    def draw_boundaries(self):
        for i in range(len(self.boundaries)):
            x1, y1 = self.boundaries[i]
            x2, y2 = self.boundaries[(i + 1) % len(self.boundaries)]
            self.gui.canvas.create_line(x1, y1, x2, y2, fill='black')

    def draw_targets(self):
        for target in self.targets:
            x, y = target.position
            self.gui.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=target.color)

    def create_targets(self, target_data):
        self.targets = [Target(position, color) for position, color in target_data]
        self.gui.clear_canvas()
        self.draw_boundaries()
        self.draw_targets()

    def check_target_reached(self, robot_position):
        for target in self.targets:
            if self._is_within_radius(robot_position, target.position, radius=4):
                return True
        return False

    def remove_target(self, robot_position):
        self.targets = [target for target in self.targets if
                        not self._is_within_radius(robot_position, target.position, radius=4)]
        self.gui.clear_canvas()
        self.draw_boundaries()
        self.draw_targets()

    def _is_within_radius(self, pos1, pos2, radius):
        return math.hypot(pos1[0] - pos2[0], pos1[1] - pos2[1]) <= radius

    def get_positions(self, current_position):
        positions = [{'current': current_position}]
        for target in self.targets:
            positions.append({'name': target.color, 'coordinate': target.position})
        return positions
