import unittest
import csv
import os
from record import save_input

class TestRecord(unittest.TestCase):
    def setUp(self):
        self.filename = 'test_record.csv'
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_save_input(self):
        input_text = "Move to (150, 150)"
        trajectories = [(150, 150)]
        thetas = [(0.5, 1.0)]
        save_input(input_text, trajectories, thetas)
        with open(self.filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0][0], input_text)
            self.assertEqual(eval(rows[0][1]), trajectories[0])
            self.assertEqual(eval(rows[0][2]), thetas[0])

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

if __name__ == '__main__':
    unittest.main()
