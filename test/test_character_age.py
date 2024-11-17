"""Test the character age calculation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import unittest
from nvlib.model.data.date_time_tools import get_age


class NrmOpr(unittest.TestCase):

    def testBirthday(self):
        self.assertEqual(get_age('2015-09-08', '1989-09-08', '2018-04-20'), 26)
        self.assertEqual(get_age('2016-09-08', '1989-09-08', '2019-04-20'), 27)
        self.assertEqual(get_age('2016-02-01', '1989-02-01', '2019-04-20'), 27)

    def testOneDayBefore(self):
        self.assertEqual(get_age('2015-09-07', '1989-09-08', '2018-04-20'), 25)
        self.assertEqual(get_age('2016-09-07', '1989-09-08', '2019-04-20'), 26)
        self.assertEqual(get_age('2016-01-31', '1989-02-01', '2019-04-20'), 26)

    def testDead(self):
        self.assertEqual(get_age('2019-04-20', '1989-09-08', '2018-04-20'), -1)
        self.assertEqual(get_age('2028-04-20', '1989-09-08', '2018-04-20'), -10)
        self.assertEqual(get_age('2019-04-19', '1989-09-08', '2018-04-20'), 0)

    def testMissing(self):
        self.assertEqual(get_age('2028-04-20', None, '2018-04-20'), -10)
        # "now" is after the death date, so the birth date isn't needed
        self.assertRaises(TypeError, lambda:get_age('2015-09-08', None, '2018-04-20'))
        # "now" is before the death date, so the birth date is needed
        self.assertRaises(TypeError, lambda:get_age('2016-09-08', None, None))
        # neither birth date nor death date is given
        self.assertRaises(TypeError, lambda:get_age(None, '1989-02-01', '2019-04-20'))
        # no "Now" given

    def testMalformed(self):
        self.assertRaises(ValueError, lambda:get_age('2015-09', '1989-09-08', '2018-04-20'))
        self.assertRaises(ValueError, lambda:get_age('2015-09-08', '1989-09', '2018-04-20'))
        self.assertRaises(ValueError, lambda:get_age('2015-09-08', '1989-09-08', '2018-04'))

    def testInvalid(self):
        self.assertRaises(ValueError, lambda:get_age('2015-09-08', '1989-09-32', '2018-04-20'))
        self.assertRaises(ValueError, lambda:get_age('2015-09-32', '1989-09-08', '2018-04-20'))
        self.assertRaises(ValueError, lambda:get_age('2015-09-08', '1989-09-08', '2018-04-32'))
        self.assertRaises(ValueError, lambda:get_age('0000-09-08', '1989-09-08', '2018-04-20'))


if __name__ == "__main__":
    unittest.main()
