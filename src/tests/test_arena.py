import unittest
from arena import Arena, Target
from display import GUI

class TestArena(unittest.TestCase):
    def setUp(self):
        self.gui = GUI()
        boundaries = [(0, 0), (0, 400), (400, 400), (400, 0)]
        self.arena = Arena(self.gui, boundaries)

    def test_initial_targets(self):
        self.assertEqual(len(self.arena.targets), 0)

    def test_create_targets(self):
        target_data = [((150, 150), 'red'), ((200, 200), 'green'), ((250, 250), 'blue')]
        self.arena.create_targets(target_data)
        self.assertEqual(len(self.arena.targets), 3)
        self.assertEqual(self.arena.targets[0].color, 'red')
        self.assertEqual(self.arena.targets[0].position, (150, 150))

    def test_check_target_reached(self):
        target_data = [((150, 150), 'red')]
        self.arena.create_targets(target_data)
        self.assertTrue(self.arena.check_target_reached((150, 150)))
        self.assertFalse(self.arena.check_target_reached((100, 100)))

    def test_remove_target(self):
        target_data = [((150, 150), 'red')]
        self.arena.create_targets(target_data)
        self.arena.remove_target((150, 150))
        self.assertEqual(len(self.arena.targets), 0)

if __name__ == '__main__':
    unittest.main()
