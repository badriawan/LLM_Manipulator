import matplotlib.pyplot as plt
from robot import Robot
from display import GUI
import transformation


class MockArena:
    def draw_boundaries(self):
        pass

    def draw_targets(self):
        pass


def draw_reachable_region(robot, step_size=10):
    reachable_points = []
    for x in range(-400, 400, step_size):
        for y in range(-400, 400, step_size):
            if transformation.is_reachable(robot, x + 200, y + 200):
                reachable_points.append((x + 200, y + 200))

    # Plotting reachable points
    x_coords, y_coords = zip(*reachable_points)
    plt.scatter(x_coords, y_coords, s=10, c='blue', marker='o', label='Reachable')
    plt.title('Reachable Region')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    gui = GUI()
    arena = MockArena()
    robot = Robot(gui, arena)
    draw_reachable_region(robot)
