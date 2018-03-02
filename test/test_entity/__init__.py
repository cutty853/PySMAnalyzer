#!/usr/bin/python
# coding: utf-8

"""
  entity test module
"""

# Disable "UPPER_CASE at top level" linter infos
# pylint: disable=C0103

import unittest
from . import test_function

loader = unittest.TestLoader()
test_function_suite = loader.loadTestsFromModule(test_function)
