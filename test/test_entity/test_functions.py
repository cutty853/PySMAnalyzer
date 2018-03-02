# coding: utf-8

"""
  Test module for the entity.function module
"""

import unittest
from lxml import etree

import entity.functions as functions


class TestFunction(unittest.TestCase):
    """ Test case for the Function class in the entity.functions module """
    def shortDescription(self):
        return None

    def test___str__(self):
        my_func = functions.Function(r"STV\Trieuse\stv\src\ttpdsext.c",
                                    "initttpdsext()")
        final_string =  \
            r"Function called initttpdsext() in STV\Trieuse\stv\src\ttpdsext.c"
        metrics_final_string = final_string + \
            " has following metrics:\n" + \
            "  complexity: 6\n" + "  statements: 25\n" + \
            "  maximum_depth: 4\n" + "  calls: 0"

        # Basic string output (without metrics)
        self.assertEqual(str(my_func), final_string)

        # Complex string ouput (with metrics)
        tree = etree.parse("samples/sample.xml")
        my_func.load_metrics(tree)
        self.assertEqual(str(my_func), metrics_final_string)

    def test_load_metrics(self):
        """ test the load_metrics method """
        tree = etree.parse("samples/sample.xml")
        my_func = functions.Function(r"STV\Trieuse\stv\src\ttpdsext.c",
                                    "initttpdsext()")
        # The asked function doesn't exist in the sample file
        my_bad_func = functions.Function(r"STV\Trieuse\stv\src\ttpdsext.c",
                                        "initttpxt()")

        with self.assertRaises(functions.FunctionNotFound):
            my_bad_func.load_metrics(tree)

        my_func.load_metrics(tree)
        self.assertEqual(my_func.metrics.complexity, 6)
        self.assertEqual(my_func.metrics.statements, 25)
        self.assertEqual(my_func.metrics.maximum_depth, 4)
        self.assertEqual(my_func.metrics.calls, 0)
