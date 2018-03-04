# coding: utf-8

"""
  reader test module
"""

# Disable "UPPER_CASE at top level" linter infos
# pylint: disable=C0103

import unittest
from . import test_smreader
from . import test_rules_reader

loader = unittest.TestLoader()
test_smreader_suite = loader.loadTestsFromModule(test_smreader)
test_rules_reader_suite = loader.loadTestsFromModule(test_rules_reader)
