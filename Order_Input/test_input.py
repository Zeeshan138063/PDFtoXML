import unittest
import input
import exemel

#create a test class that inherits from unittest.TestCase

class TestLearn(unittest.TestCase):

    def test_formatted_weeks(self): #method must start with the word test, so this module knows that it is a test.
        actual_1 = exemel.get_formatted_weeks(["3/19", "3/26", "4/9"])
        actual_2 = exemel.get_formatted_weeks(["5/7", "6/4", "7/9", "8/13"])

        expected_1 = ['2018-03-19', '2018-03-26', '2018-04-09']
        expected_2 = ['2018-05-07', '2018-06-04', '2018-07-09', '2018-08-13']

        self.assertListEqual(actual_1, expected_1)
        self.assertListEqual(actual_2, expected_2)

    def test_get_start_time(self):
        actual_1 = exemel.get_start_time("MTuWThF  5:30a- 9:00a")
        actual_2 = exemel.get_start_time("MTuWThF 5:15a-9:45a")
        actual_3 = exemel.get_start_time("MTuW 12:15a-9:45a")

        expected_1 = "05:30"
        expected_2 = "05:15"
        expected_3 = "00:15"

        self.assertEqual(actual_1,expected_1)
        self.assertEqual(actual_2, expected_2)
        self.assertEqual(actual_3, expected_3)

    def test_get_end_time(self):
        actual_1 = exemel.get_end_time("MTuWThF  5:30a- 9:00a")
        actual_2 = exemel.get_end_time("MTuWThF 5:15a-9:45a")
        actual_3 = exemel.get_end_time("MTuW 12:15a-12:00p")

        expected_1 = "09:00"
        expected_2 = "09:45"
        expected_3 = "12:00"

        self.assertEqual(actual_1, expected_1)
        self.assertEqual(actual_2, expected_2)
        self.assertEqual(actual_3, expected_3)


if __name__ == "__main__": # this allows us to run python test_learn.py and will give us the same result as above.
    unittest.main()



