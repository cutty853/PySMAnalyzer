#!/usr/bin/python
# coding: utf-8

"""
  Test module for the entity.function module
"""

import unittest
from lxml import etree

import entity.function as function


class TestFunction(unittest.TestCase):
    """ Test case for the Function class in the entity.function module """
    def shortDescription(self):
        return None

    def test_load_metrics(self):
        """ test the load_metrics method """
        my_func = function.Function(r"STV\Trieuse\stv\src\ttpdsext.c",
                                    "initttpdsext()")
        try:
            tree = etree.parse("samples/sample.xml")
        except OSError:
            print("samples/sample.xml doesn't exist you should not erase it")
            print("since this file is needed for the unittest of the project")
            print("\n\n\n")
            raise

        my_func = function.Function(r"STV\Trieuse\stv\src\ttpdsext.c",
                                    "initttpdsext()")

        # The asked function doesn't exist in the sample file
        my_bad_func = function.Function(r"STV\Trieuse\stv\src\ttpdsext.c",
                                        "initttpxt()")

        with self.assertRaises(function.FunctionNotFound):
            my_bad_func.load_metrics(tree)

        my_func.load_metrics(tree)
        self.assertEqual(my_func.metrics.complexity, 6)
        self.assertEqual(my_func.metrics.statements, 25)
        self.assertEqual(my_func.metrics.maximum_depth, 4)
        self.assertEqual(my_func.metrics.calls, 0)
