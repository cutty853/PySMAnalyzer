# coding: utf-8

"""
  Importation module for the unit-test of the project
"""

import unittest

from . import test_entity
from . import test_reader
from . import test_writer
from . import test_utils
from . import test_analyzer


def run():
    """ Runner of the test suite """
    # List all the TestCase to import in the test suite
    tests = []
    tests.append(test_entity.test_functions_suite)
    tests.append(test_entity.test_files_suite)
    tests.append(test_entity.test_metrics_suite)
    tests.append(test_entity.test_reports_suite)

    tests.append(test_reader.test_smreader_suite)
    tests.append(test_reader.test_rules_reader_suite)

    tests.append(test_writer.test_htmlreport_suite)

    tests.append(test_utils.create_test_suite())

    tests.append(test_analyzer.create_test_suite())

    # Define the final TestSuite
    test_suite = unittest.TestSuite(tests)

    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(test_suite)
