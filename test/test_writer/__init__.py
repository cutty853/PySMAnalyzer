# coding: utf-8

"""
  reader test module
"""

# Disable "UPPER_CASE at top level" linter infos
# pylint: disable=C0103

import unittest
from . import test_htmlreport

loader = unittest.TestLoader()
test_htmlreport_suite = loader.loadTestsFromModule(test_htmlreport)
