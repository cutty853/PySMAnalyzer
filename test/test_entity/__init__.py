#!/usr/bin/python
# coding: utf-8

"""
  entity test module
"""

# Disable "UPPER_CASE at top level" linter infos
# pylint: disable=C0103

import unittest
from . import test_functions
from . import test_metrics

loader = unittest.TestLoader()
test_functions_suite = loader.loadTestsFromModule(test_functions)
test_metrics_suite = loader.loadTestsFromModule(test_metrics)
