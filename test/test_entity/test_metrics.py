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

    def setUp(self):
        self.test_metrics = metrics.FileMetrics({
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

    def tearDown(self):
        del self.test_metrics

    def test___str__(self):
        """ String conversion test """
        metrics_string = \
            "M0: 461; M1: 289; M2: 24.6; M3: 16.3; M4: 6; M5: 42.7; " + \
            "M6: 88; M7: progexplttpdsext(); M8: 78; M9: 328; " + \
            "M10: 9+; M11: 5.51; M12: 17.0"
        self.assertEqual(str(self.test_metrics), metrics_string)

    def test_get(self):
        """ Test the get method of FileMetrics object """
        self.assertEqual(self.test_metrics.get("M1"), 289)
        # Also testing for string...
        self.assertEqual(self.test_metrics.get("M7"), "progexplttpdsext()")


class TestFunctionMetrics(unittest.TestCase):
    """docstring for TestFunctionMetrics """

    def shortDescription(self):
        return None

    def setUp(self):
        self.test_metrics = metrics.FunctionMetrics(7, 25, 3, 5)

    def test___str__(self):
        """ String conversion test """
        metrics_string = \
            "complexity: 7; statements: 25; maximum_depth: 3; calls: 5"
        self.assertEqual(str(self.test_metrics), metrics_string)
