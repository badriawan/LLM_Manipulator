import unittest
from transformation import extend_to_square, is_reachable
from robot import Robot
from display import GUI
from arena import Arena

class TestTransformationFunctions(unittest.TestCase):

    def setUp(self):
        # Set up a GUI and arena for the Robot instance (needed for is_reachable)
        self.gui = GUI()
        self.boundaries = [(0, 0), (0, 400), (400, 400), (400, 0)]
        self.arena = Arena(self.gui, self.boundaries)
        self.robot = Robot(self.gui, self.arena, link_length1=100, link_length2=100)

    def test_extend_to_square(self):
        x, y = 300, 300
        step_size = 50
        expected_square = [
            (250, 250),
            (350, 250),
            (250, 350),
            (350, 350)
        ]
        square = extend_to_square(x, y, step_size)
        self.assertEqual(square, expected_square)

    def test_is_reachable(self):
        # Test if coordinate (300, 300) is reachable
        self.assertTrue(is_reachable(self.robot, 300, 300))

        # Test if coordinate (400, 400) is not reachable due to angle constraints
        self.assertFalse(is_reachable(self.robot, 400, 400))

        # Test if coordinate (100, 100) is reachable
        self.assertTrue(is_reachable(self.robot, 100, 100))

        # Test if coordinate (0, 400) is not reachable due to distance
        self.assertFalse(is_reachable(self.robot, 0, 400))

if __name__ == '__main__':
    unittest.main()
