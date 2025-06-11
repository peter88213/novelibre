"""Test the character age calculation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import unittest
from nvlib.model.data.py_calendar import PyCalendar


class NrmOpr(unittest.TestCase):

    def testBirthday(self):
        self.assertEqual(PyCalendar.age(
            '2015-09-08', '1989-09-08', '2018-04-20'),
            (26, None, 9496, None))
        self.assertEqual(PyCalendar.age(
            '2016-09-08', '1989-09-08', '2019-04-20'),
            (27, None, 9862, None))
        self.assertEqual(PyCalendar.age(
            '2016-02-01', '1989-02-01', '2019-04-20'),
            (27, None, 9861, None))

    def testOneDayBefore(self):
        self.assertEqual(PyCalendar.age(
            '2015-09-07', '1989-09-08', '2018-04-20'),
            (25, None, 9495, None))
        self.assertEqual(PyCalendar.age(
            '2016-09-07', '1989-09-08', '2019-04-20'),
            (26, None, 9861, None))
        self.assertEqual(PyCalendar.age(
            '2016-01-31', '1989-02-01', '2019-04-20'),
            (26, None, 9860, None))

    def testDead(self):
        self.assertEqual(PyCalendar.age(
            '2019-04-20', '1989-09-08', '2018-04-20'),
            (28, 1, None, 365))
        self.assertEqual(PyCalendar.age(
            '2028-04-20', '1989-09-08', '2018-04-20'),
            (28, 10, None, 3653))
        self.assertEqual(PyCalendar.age(
            '2019-04-19', '1989-09-08', '2018-04-20'),
            (28, 0, None, 364))

    def testMissing(self):
        self.assertEqual(PyCalendar.age(
            '2028-04-20', None, '2018-04-20'),
            (None, 10, None, 3653))
        # "now" is after the death date, so the birth date isn't needed

        self.assertRaises(UnboundLocalError, lambda:PyCalendar.age('2015-09-08', None, '2018-04-20'))
        # "now" is before the death date, so the birth date is needed

        self.assertRaises(UnboundLocalError, lambda:PyCalendar.age('2016-09-08', None, None))
        # neither birth date nor death date is given

        self.assertRaises(TypeError, lambda:PyCalendar.age(None, '1989-02-01', '2019-04-20'))
        # no "Now" given

    def testMalformed(self):
        self.assertRaises(ValueError, lambda:PyCalendar.age('2015-09', '1989-09-08', '2018-04-20'))
        self.assertRaises(ValueError, lambda:PyCalendar.age('2015-09-08', '1989-09', '2018-04-20'))
        self.assertRaises(ValueError, lambda:PyCalendar.age('2015-09-08', '1989-09-08', '2018-04'))

    def testInvalid(self):
        self.assertRaises(ValueError, lambda:PyCalendar.age('2015-09-08', '1989-09-32', '2018-04-20'))
        self.assertRaises(ValueError, lambda:PyCalendar.age('2015-09-32', '1989-09-08', '2018-04-20'))
        self.assertRaises(ValueError, lambda:PyCalendar.age('2015-09-08', '1989-09-08', '2018-04-32'))
        self.assertRaises(ValueError, lambda:PyCalendar.age('0000-09-08', '1989-09-08', '2018-04-20'))


if __name__ == "__main__":
    unittest.main()
