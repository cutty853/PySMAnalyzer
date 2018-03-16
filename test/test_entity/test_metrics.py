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

    def test_is_metric_treatable(self):
        """ test for the is_metric_valid function """
        self.assertTrue(metrics.is_metric_treatable(2))
        self.assertFalse(metrics.is_metric_treatable("9+"))
        self.assertFalse(metrics.is_metric_treatable(""))
        self.assertFalse(metrics.is_metric_treatable("disable"))

    def test___str__(self):
        """ String conversion test """
        metrics_string = \
            "M0: 461; M1: 289; M2: 24.6; M3: 16.3; M4: 6; M5: 42.7; " + \
            "M6: 88; M7: progexplttpdsext(); M8: 78; M9: 328; " + \
            "M10: 9+; M11: 5.51; M12: 17.0"
        self.assertEqual(str(self.test_metrics), metrics_string)

    def test___iter__(self):
        """ Test for iterator """
        true_metrics = (
            ("M0", 461), ("M1", 289), ("M2", 24.6), ("M3", 16.3),
            ("M4", 6), ("M5", 42.7), ("M6", 88), ("M7", "progexplttpdsext()"),
            ("M8", 78), ("M9", 328), ("M10", "9+"), ("M11", 5.51),
            ("M12", 17.0)
        )
        for metric, true_metric in zip(self.test_metrics, true_metrics):
            self.assertTupleEqual(metric, true_metric)

    def test_get(self):
        """ Test the get method of FileMetrics object """
        self.assertEqual(self.test_metrics.get("M1"), 289)
        # Also testing for string...
        self.assertEqual(self.test_metrics.get("M7"), "progexplttpdsext()")

    def test_set(self):
        """ Test the set method of FileMetrics class """
        self.test_metrics.set("M0", 450)
        self.assertEqual(self.test_metrics.get("M0"), 450)
        self.test_metrics.set("M7", "my_func")
        self.assertEqual(self.test_metrics.get("M7"), "my_func")


class TestFunctionMetrics(unittest.TestCase):
    """docstring for TestFunctionMetrics """

    def shortDescription(self):
        return None

    def setUp(self):
        self.test_metrics = metrics.FunctionMetrics(7, 25, 3, 5)

    def tearDown(self):
        del self.test_metrics

    def test___str__(self):
        """ String conversion test """
        metrics_string = \
            "complexity: 7; statements: 25; maximum_depth: 3; calls: 5"
        self.assertEqual(str(self.test_metrics), metrics_string)

    def test___iter__(self):
        """ iterator test """
        for metric, value in zip(self.test_metrics, (7, 25, 3, 5)):
            self.assertEqual(metric, value)

    def test_setters(self):
        """ Test all the setter of the FunctionMetrics class """
        self.test_metrics.set_complexity(10)
        self.test_metrics.set_statements(10)
        self.test_metrics.set_maximum_depth(10)
        self.test_metrics.set_calls(10)

        self.assertEqual(self.test_metrics.complexity, 10)
        self.assertEqual(self.test_metrics.statements, 10)
        self.assertEqual(self.test_metrics.maximum_depth, 10)
        self.assertEqual(self.test_metrics.calls, 10)
