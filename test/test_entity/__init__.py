# coding: utf-8

"""
  entity test module
"""

# Disable "UPPER_CASE at top level" linter infos
# pylint: disable=C0103

import unittest
from . import test_functions
from . import test_metrics
from . import test_files
from . import test_reports


loader = unittest.TestLoader()
test_functions_suite = loader.loadTestsFromModule(test_functions)
test_files_suite = loader.loadTestsFromModule(test_files)
test_metrics_suite = loader.loadTestsFromModule(test_metrics)
test_reports_suite = loader.loadTestsFromModule(test_reports)
