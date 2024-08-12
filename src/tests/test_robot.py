import unittest
from robot import Robot
from display import GUI

class TestRobot(unittest.TestCase):
    def setUp(self):
        self.gui = GUI()
        self.robot = Robot(self.gui)

    def test_initial_position(self):
        self.assertEqual(self.robot.joint1, (200, 200))
        self.assertEqual(self.robot.joint2, (300, 200))
        self.assertEqual(self.robot.end_effector, (400, 200))

    def test_inverse_kinematics(self):
        theta1, theta2 = self.robot.inverse_kinematics((150, 150))
        self.assertIsInstance(theta1, float)
        self.assertIsInstance(theta2, float)

    def test_forward_kinematics(self):
        joints = self.robot.forward_kinematics(0, 0)
        self.assertEqual(joints[1], (300, 200))
        self.assertEqual(joints[2], (400, 200))

    def test_move(self):
        thetas = self.robot.move((150, 150))
        self.assertIsInstance(thetas, list)
        self.assertEqual(len(thetas), 2)

if __name__ == '__main__':
    unittest.main()
