# coding: utf-8

"""
  Importation module for the unit-test of the project
"""

import unittest

from . import test_entity


def run():
    """ Runner of the test suite """
    # List all the TestCase to import in the test suite
    tests = []
    tests.append(test_entity.test_functions_suite)
    tests.append(test_entity.test_files_suite)
    tests.append(test_entity.test_metrics_suite)

    # Define the final TestSuite
    test_suite = unittest.TestSuite(tests)

    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(test_suite)
