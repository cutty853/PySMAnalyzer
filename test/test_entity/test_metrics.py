# coding: utf-8

"""
  Test module for the entity.metrics module
"""

import unittest
import entity.metrics as metrics

class TestFileMetrics(unittest.TestCase):
    """docstring for TestFileMetrics """

    def shortDescription(self):
        return None

    def test___str__(self):
        """ String conversion test """
        my_metrics = metrics.FileMetrics({
            "M0": 461,
            "M1": 289,
            "M2": 24.6,
            "M3": 16.3,
            "M4": 6,
            "M5": 42.7,
            "M6": 88,
            "M7": "progexplttpdsext()",
            "M8": 78,
            "M9": 328,
            "M10": "9+",
            "M11": 5.51,
            "M12": 17.0
        })
        metrics_string = \
            "M0: 461; M1: 289; M2: 24.6; M3: 16.3; M4: 6; M5: 42.7; " + \
            "M6: 88; M7: progexplttpdsext(); M8: 78; M9: 328; " + \
            "M10: 9+; M11: 5.51; M12: 17.0"
        self.assertEqual(str(my_metrics), metrics_string)

    def test_get(self):
        """ Test the get method of FileMetrics object """
        my_metrics = metrics.FileMetrics({
            "M0": 461,
            "M1": 289,
            "M2": 24.6,
            "M3": 16.3,
            "M4": 6,
            "M5": "progexplttpdsext()",
        })
        self.assertEqual(my_metrics.get("M1"), 289)
        # Also testing for string...
        self.assertEqual(my_metrics.get("M5"), "progexplttpdsext()")


class TestFunctionMetrics(unittest.TestCase):
    """docstring for TestFunctionMetrics """

    def shortDescription(self):
        return None

    def test___str__(self):
        """ String conversion test """
        my_metrics = metrics.FunctionMetrics(7, 25, 3, 5)
        metrics_string = \
            "complexity: 7; statements: 25; maximum_depth: 3; calls: 5"
        self.assertEqual(str(my_metrics), metrics_string)
