#!/usr/bin/python
# coding: utf-8

"""
  Test module for the entity.metrics module
"""

import unittest
import entity.metrics as metrics


class TestMetrics(unittest.TestCase):
    """docstring for TestMetrics."""

    def shortDescription(self):
        return None

    def test___str__(self):
        """ String conversion test """
        my_metrics = metrics.FunctionMetrics(7, 25, 3, 5)
        metrics_string = \
            "complexity: 7; statements: 25; maximum_depth: 3; calls: 5"
        self.assertEqual(str(my_metrics), metrics_string)
