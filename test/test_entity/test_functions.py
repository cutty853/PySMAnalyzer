# coding: utf-8

"""
  Test module for the entity.functions module
"""

import unittest
from lxml import etree

import entity.functions as functions


class TestFunction(unittest.TestCase):
    """ Test case for the Function class in the entity.functions module """
    def shortDescription(self):
        return None

    def setUp(self):
        self.tree = etree.parse("samples/sample.xml")
        self.test_func = functions.Function(
            r"STV\Trieuse\stv\src\ttpdsext.c", "initttpdsext()"
        )

    def tearDown(self):
        del self.tree
        del self.test_func

    def test___str__(self):
        """ string conversion test """
        final_string =  \
            r"Function called initttpdsext() in STV\Trieuse\stv\src\ttpdsext.c"
        metrics_final_string = final_string + \
            " has following metrics:\n" + \
            "  complexity: 6\n" + "  statements: 25\n" + \
            "  maximum_depth: 4\n" + "  calls: 0"

        # Basic string output (without metrics)
        self.assertEqual(str(self.test_func), final_string)

        # Complex string ouput (with metrics)
        self.test_func.load_metrics(self.tree)
        self.assertEqual(str(self.test_func), metrics_final_string)

    def test_load_metrics(self):
        """ test the load_metrics method """
        # The asked function doesn't exist in the sample file
        my_bad_func = functions.Function(
            r"STV\Trieuse\stv\src\ttpdsext.c", "initttpxt()"
        )

        with self.assertRaises(functions.FunctionNotFound):
            my_bad_func.load_metrics(self.tree)

        self.test_func.load_metrics(self.tree)
        self.assertEqual(self.test_func.metrics.complexity, 6)
        self.assertEqual(self.test_func.metrics.statements, 25)
        self.assertEqual(self.test_func.metrics.maximum_depth, 4)
        self.assertEqual(self.test_func.metrics.calls, 0)
