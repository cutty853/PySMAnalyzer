#!/usr/bin/python
# coding: utf-8

"""
  MODULE DOCUMENTATION
"""

import unittest
import utils


class TestUtils(unittest.TestCase):
    """ TestCase for the utils module """

    def shortDescription(self):
        return None

    def test_center(self):
        """ Test for the center function used to center text on screen """
        my_message = "Hello I'm a test message"
        self.assertEqual(
            utils.center(my_message, 30),
            "   Hello I'm a test message   "
        )
        self.assertEqual(
            utils.center(my_message, 20),
            "Hello I'm a test message"
        )

        # NOTE: On odd lenght final size won't be equal to max_line_size
        my_odd_message = "Hello I have a test message"
        self.assertEqual(
            utils.center(my_odd_message, 30),
            " Hello I have a test message "
        )


def run():
    """ main du programme """
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestUtils)
    unittest.TextTestRunner(verbosity=2).run(test_suite)
